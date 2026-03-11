import streamlit as st
import anthropic                          # CHANGED: was "from openai import OpenAI"
from pypdf import PdfReader
from docx import Document

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="SystemLens",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
    """
    <style>
    /* =========================
       Base App Theme
    ========================== */
    .stApp {
        background: linear-gradient(180deg, #0b1220 0%, #111827 100%);
        color: #e5e7eb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    p, label {
        color: #e5e7eb !important;
    }

    /* =========================
       Hero Section
    ========================== */
    /* =========================
   New Hero Section
========================== */
    .hero-wrapper {
        background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,41,59,0.92));
        border: 1px solid rgba(56,189,248,0.18);
        border-radius: 24px;
        padding: 32px;
        margin-bottom: 1.5rem;
        box-shadow: 0 16px 40px rgba(0,0,0,0.28);
    }
    
    .hero-topline {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(56,189,248,0.12);
        color: #7dd3fc;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .hero-main-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        line-height: 1.1;
    }
    
    .hero-highlight {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-description {
        font-size: 1.02rem;
        color: #cbd5e1;
        line-height: 1.7;
        max-width: 820px;
        margin-bottom: 1.25rem;
    }
    
    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 10px;
    }
    
    .hero-badge {
        background: rgba(148,163,184,0.12);
        border: 1px solid rgba(148,163,184,0.16);
        color: #e2e8f0;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 0.88rem;
        font-weight: 500;
    }
    
    .hero-footer-note {
        margin-top: 14px;
        color: #94a3b8;
        font-size: 0.86rem;
    }
    /* =========================
       Feature Cards
    ========================== */
    .feature-card {
        background: rgba(30,41,59,0.72);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 18px;
        padding: 18px;
        min-height: 120px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }

    .feature-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.4rem;
    }

    .feature-text {
        font-size: 0.92rem;
        color: #cbd5e1;
        line-height: 1.5;
    }

    /* =========================
       Content Cards
    ========================== */
    .section-card {
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 20px;
        padding: 22px;
        margin-top: 1rem;
        box-shadow: 0 8px 28px rgba(0,0,0,0.22);
    }

    .small-note {
        color: #94a3b8;
        font-size: 0.86rem;
        margin-top: 0.35rem;
    }

    .divider {
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        border-top: 1px solid rgba(148,163,184,0.16);
    }

    /* =========================
       Inputs
    ========================== */
    .stTextInput input,
    .stTextArea textarea {
        background-color: #0f172a !important;
        color: #e5e7eb !important;
        -webkit-text-fill-color: #e5e7eb !important;
        border-radius: 12px !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* =========================
       Selectbox
    ========================== */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        border-radius: 12px !important;
        color: #e5e7eb !important;
    }

    .stSelectbox div[data-baseweb="select"] span {
        color: #e5e7eb !important;
    }

    .stSelectbox svg {
        fill: #e5e7eb !important;
    }

    /* =========================
       Buttons
    ========================== */
    .stButton > button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1);
        color: #ffffff !important;
        border: none;
        border-radius: 12px;
        padding: 0.65rem 1.4rem;
        font-weight: 700;
        box-shadow: 0 8px 18px rgba(14,165,233,0.18);
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        color: #ffffff !important;
    }

    /* =========================
       File Uploader
    ========================== */
    .stFileUploader {
        background: transparent !important;
        border-radius: 14px;
        padding: 0;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #f8fafc !important;
        border: 1px solid rgba(239, 68, 68, 0.85) !important;
        border-radius: 18px !important;
        padding: 14px !important;
    }

    [data-testid="stFileUploaderDropzone"] div,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small,
    [data-testid="stFileUploaderDropzone"] p {
        color: #475569 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #475569 !important;
    }

    .stFileUploader button {
        background: linear-gradient(90deg, #0ea5e9, #6366f1) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
    }

    .stFileUploader button:hover {
        background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
        color: #ffffff !important;
    }

    [data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
        color: #e5e7eb !important;
        -webkit-text-fill-color: #e5e7eb !important;
        font-weight: 600 !important;
    }

    [data-testid="stFileUploader"] small {
        color: #cbd5e1 !important;
        -webkit-text-fill-color: #cbd5e1 !important;
    }

    /* =========================
       Spinner / Status Cleanup
    ========================== */
    [data-testid="stStatusWidget"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    [data-testid="stAlert"],
    [data-testid="stNotification"] {
        background: rgba(15, 23, 42, 0.72) !important;
        color: #e5e7eb !important;
        border-radius: 14px !important;
        border: 1px solid rgba(56,189,248,0.18) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Anthropic client                        # CHANGED: was OpenAI(api_key=...)
# -----------------------------
api_key = st.secrets["ANTHROPIC_API_KEY"] # CHANGED: was "OPENAI_API_KEY"
client = anthropic.Anthropic(api_key=api_key)

# -----------------------------
# Helper functions
# -----------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text

def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")

def extract_artifact_text(uploaded_file):
    if uploaded_file is None:
        return ""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif file_name.endswith((".txt", ".cbl", ".cob", ".cpy")):
        return extract_text_from_txt(uploaded_file)
    else:
        return ""

# -----------------------------
# Header / Hero section
# -----------------------------
st.markdown(
    """
<div class="hero-wrapper">
    <div class="hero-topline">AI Product Prototype • Enterprise Systems • Legacy Modernization</div>
    <div class="hero-main-title">🔎 <span class="hero-highlight">SystemLens</span></div>
    <div class="hero-description">
        Understand enterprise systems, technical artifacts, and legacy code faster.
        Upload a document or paste a workflow to analyze dependencies, assess release impact,
        generate onboarding summaries, and break down COBOL logic into business-readable explanations.
    </div>
    <div class="hero-badges">
        <div class="hero-badge">Explain Artifacts</div>
        <div class="hero-badge">Trace Dependencies</div>
        <div class="hero-badge">Assess Change Impact</div>
        <div class="hero-badge">Onboarding Summaries</div>
        <div class="hero-badge">COBOL Breakdown</div>
    </div>
    <div class="hero-footer-note">
        Designed to help engineers, TPMs, PMs, and modernization teams make sense of complex systems.
    </div>
</div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Feature cards
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">⚙️ Explain Systems</div>
            <div class="feature-text">
                Turn technical artifacts into clear system and workflow understanding.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🔗 Trace Dependencies</div>
            <div class="feature-text">
                Surface upstream and downstream connections before making changes.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🧠 Decode Legacy Logic</div>
            <div class="feature-text">
                Translate COBOL and legacy flows into business-readable explanations.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# -----------------------------
# Input section
# -----------------------------
analysis_mode = st.selectbox(
    "🔍 Choose analysis mode",
    [
        "Explain Artifact",
        "Dependency Analysis",
        "Change Impact Analysis",
        "Onboarding Summary",
        "COBOL Breakdown"
    ]
)

uploaded_file = st.file_uploader(
    "Upload a PDF, Word document, text file, or COBOL source file",
    type=["pdf", "docx", "txt", "cbl", "cob", "cpy"]
)

st.markdown(
    '<div class="small-note">Best results with text-based PDFs, DOCX files, and structured technical documents.</div>',
    unsafe_allow_html=True
)

artifact = st.text_area(
    "Or paste code, architecture notes, API documentation, or process notes",
    height=260,
    placeholder="Paste a workflow, architecture note, service interaction, requirement document excerpt, or process description here..."
)

question = st.text_input(
    "Ask a question",
    placeholder="Example: Give me a beginner-friendly summary of this flow"
)

run_clicked = st.button("Run Analysis")

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# AI logic
# -----------------------------
if run_clicked:
    extracted_text = extract_artifact_text(uploaded_file) if uploaded_file else ""
    final_artifact = extracted_text if extracted_text.strip() else artifact

    if not final_artifact or not question:
        st.warning("Please upload a file or paste an artifact, and enter a question.")
    else:
        try:
            if analysis_mode == "Explain Artifact":
                mode_instruction = """
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
"""

            elif analysis_mode == "Dependency Analysis":
                mode_instruction = """
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
"""

            elif analysis_mode == "Change Impact Analysis":
                mode_instruction = """
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
"""
            elif analysis_mode == "COBOL Breakdown":
                mode_instruction = """
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
"""

            else:  # Onboarding Summary
                mode_instruction = """
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
"""

            prompt = f"""
You are an enterprise systems analyst helping a new engineer understand a complex enterprise system.

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

{mode_instruction}
"""

            with st.spinner("Analyzing artifact..."):
                # CHANGED: was client.chat.completions.create(model="gpt-4.1-mini", ...)
                response = client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=4096,
                    system="You are a senior enterprise systems analyst with strong understanding of legacy enterprise systems, including COBOL-based applications. You explain technical artifacts clearly, practically, and in a structured format for new engineers, product managers, architects, and technical program managers.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )

                # CHANGED: was response.choices[0].message.content
                answer = response.content[0].text

                st.subheader(f"AI Output — {analysis_mode}")
                st.markdown(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
