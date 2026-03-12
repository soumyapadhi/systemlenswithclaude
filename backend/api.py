import io
import os
from typing import Optional

import anthropic
from docx import Document
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader

app = FastAPI(title="SystemLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ---------------------------------------------------------------------------
# File extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = Document(io.BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])


def extract_artifact_text(filename: str, file_bytes: bytes) -> str:
    name = filename.lower()
    if name.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif name.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif name.endswith((".txt", ".cbl", ".cob", ".cpy", ".jcl", ".job")):
        return file_bytes.decode("utf-8")
    return ""


# ---------------------------------------------------------------------------
# Mode instructions (exact prompts from app.py)
# ---------------------------------------------------------------------------

MODE_INSTRUCTIONS: dict[str, str] = {
    "Explain Artifact": """
Return your response in exactly this structure:

### 1. System / Module Summary
Explain in 2-3 lines what this artifact appears to do.

### 2. Key Components / Dependencies
List the main services, modules, systems, or actors mentioned or implied in the artifact.

### 3. End-to-End Workflow
Explain the likely end-to-end flow step by step in simple terms.

### 4. Simple Flow Diagram
Represent the workflow as a simple arrow diagram like this:

Customer
↓
OrderService
↓
InventoryService
↓
PaymentService
↓
NotificationService

### 5. Potential Impact if This Changes
Explain what downstream impact or risks may happen if this module or workflow changes.

### 6. Gaps / Unclear Areas
Mention what is missing, ambiguous, or would need validation from an engineer or documentation.

### 7. Program / Product Insight
Explain what a product manager or technical program manager should pay attention to in this system.
Mention risks, scaling concerns, or operational dependencies.
""",

    "Dependency Analysis": """
Return your response in exactly this structure:

### 1. Primary Module / Service
Identify the main module or service in the artifact.

### 2. Upstream Dependencies
List systems, services, inputs, or actors this module depends on.

### 3. Downstream Dependencies
List systems, services, or workflows likely affected by this module.

### 4. Dependency Risks
Mention any dependency-related risks or tight coupling visible from the artifact.

### 5. Gaps / Unclear Areas
Mention what dependency information is missing or needs confirmation.

### 6. Program / Product Insight
Explain what a PM or TPM should watch from a dependency and coordination standpoint.
""",

    "Change Impact Analysis": """
Return your response in exactly this structure:

### 1. Module / Area Being Considered
Explain what part of the system appears to be changing.

### 2. Likely Impacted Areas
List downstream systems, workflows, or business processes that may be affected.

### 3. Key Risks
Mention operational, technical, or business risks if this module changes.

### 4. Validation / Testing Recommendations
Suggest what should be validated before release.

### 5. Gaps / Unclear Areas
Mention what is missing and what needs deeper engineering review.

### 6. Program / Product Insight
Explain what a TPM should do before and during release if this area changes.
""",

    "Onboarding Summary": """
Return your response in exactly this structure:

### 1. Beginner-Friendly Summary
Explain what this artifact does in very simple terms.

### 2. Key Components to Understand First
List the main modules, systems, or actors a new joiner should focus on first.

### 3. End-to-End Workflow
Explain the flow step by step as if explaining to someone new to the system.

### 4. Simple Flow Diagram
Represent the workflow as a simple arrow diagram.

### 5. What Could Be Confusing
Call out areas that may confuse a new engineer or PM.

### 6. Suggested Next Questions
List 3-5 follow-up questions a new joiner should ask to understand the system better.

### 7. Program / Product Insight
Explain what a PM or TPM should understand about this system beyond the technical flow.
""",

    "COBOL Breakdown": """
Return your response in exactly this structure:

### 1. Program Purpose
Explain what business function this COBOL program performs.

### 2. Execution Context
Based on the structure, indicate whether this program appears to be:
- batch processing
- report generation
- transaction logic
- data transformation
If unclear, say so.

### 3. High-Level Logic Flow
Describe the program logic step by step in plain English.

### 4. Key Sections / Paragraphs
Explain the role of important divisions, sections, and paragraphs.

### 5. Inputs and Outputs
Identify:
- input files
- output files
- working storage fields
- copybooks
- tables or data sources (if visible)

### 6. Business Rules
Highlight calculations, validations, and conditional logic.

### 7. System Dependencies
Identify possible upstream or downstream dependencies such as:
- batch jobs
- reports
- reconciliation processes
- other programs

### 8. Risks If Modified
Explain what could break if this program is changed.

### 9. Modernization / Refactoring Suggestions
Suggest ways the logic could be modularized, documented, or migrated to modern architectures.

### 10. Quick Summary for New Engineers
Provide a short explanation that someone new to the system can understand quickly.

Important instructions:
- Do not invent external systems if they are not visible.
- If dependencies cannot be determined, clearly state that.
""",
}

SYSTEM_PROMPT = (
    "You are a senior enterprise systems analyst with strong understanding of legacy enterprise "
    "systems, including COBOL-based applications. You explain technical artifacts clearly, "
    "practically, and in a structured format for new engineers, product managers, architects, "
    "and technical program managers."
)

# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    analysis_mode: str = Form(...),
    question: str = Form(...),
    artifact: Optional[str] = Form(""),
    file: Optional[UploadFile] = File(None),
):
    extracted_text = ""
    if file and file.filename:
        file_bytes = await file.read()
        extracted_text = extract_artifact_text(file.filename, file_bytes)

    final_artifact = extracted_text if extracted_text.strip() else (artifact or "")

    if not final_artifact.strip() or not question.strip():
        return {"error": "Please provide an artifact (file or pasted text) and a question."}

    mode_instruction = MODE_INSTRUCTIONS.get(analysis_mode, "")

    prompt = f"""You are an enterprise systems analyst helping a new engineer understand a complex enterprise system.

Your task is to analyze the technical artifact and answer the user's question in a practical, structured, beginner-friendly way.

Important instructions:
- Use only the information available in the artifact
- Do not invent dependencies or workflows that are not supported by the input
- If something is unclear or missing, explicitly mention it
- Explain in simple business and system language, not overly technical jargon
- Keep the answer crisp but useful

Analysis mode:
{analysis_mode}

Technical artifact:
{final_artifact}

User question:
{question}

{mode_instruction}"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return {"result": response.content[0].text, "analysis_mode": analysis_mode}
