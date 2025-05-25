import streamlit as st
from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import spacy

nlp = spacy.load("en_core_web_sm")

# --- Helper Functions ---
def detect_fake_keywords(text):
    suspicious_keywords = [
        "harverd", "oxfurd", "unversity", "prestigous", "global institute of excellence",
        "cambrige", "certificate of magic", "univercity", "dummy", "sample"
    ]
    return [kw for kw in suspicious_keywords if kw.lower() in text.lower()]

def detect_missing_authentic_features(text):
    must_have = ["degree", "awarded", "certify", "university", "honors"]
    return [word for word in must_have if word.lower() not in text.lower()]

def extract_entities(text):
    doc = nlp(text)
    universities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    degrees = [ent.text for ent in doc.ents if ent.label_ in ["EDUCATION", "QUALIFICATION"]]
    return universities, degrees

def detect_degrees(text):
    degree_keywords = ["Bachelor", "Master", "PhD", "B.Sc", "M.Sc", "MBA", "B.Tech", "M.Tech", "Doctorate", "Diploma"]
    return [deg for deg in degree_keywords if deg.lower() in text.lower()]

def calculate_fake_score(text):
    score = 100
    score -= len(detect_fake_keywords(text)) * 15
    score -= len(detect_missing_authentic_features(text)) * 10
    return max(score, 0)

# --- UI Config ---
st.set_page_config(page_title="Fake Certificate Detector", layout="wide", initial_sidebar_state="expanded")

# --- Sidebar Info ---
st.sidebar.title("Instructions")
st.sidebar.markdown("""
Upload an image or PDF of a certificate. The app will:
- Extract text using OCR
- Detect fake keywords or missing terms
- Identify university/degree mentions
- Generate a fake probability score
""")

uploaded_file = st.sidebar.file_uploader("Upload Certificate File", type=["jpg", "jpeg", "png", "pdf"])
st.sidebar.markdown("---")
st.sidebar.caption("Supports image (JPG/PNG) or PDF")

# --- Main Interface ---
st.title("Fake Degree or Certificate Detector")
st.markdown("This tool analyzes scanned certificates to detect potential forgery using NLP and heuristic rules.")

if uploaded_file:
    file_type = uploaded_file.type
    text = ""

    # Horizontal layout
    doc_col, analysis_col = st.columns([1.2, 1.8])

    with doc_col:
        st.subheader("Document Preview")
        if file_type == "application/pdf":
            with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
            st.info("PDF Document Uploaded")
            st.code(text[:1000] + "..." if len(text) > 1000 else text)
        else:
            image = Image.open(uploaded_file)
            text = pytesseract.image_to_string(image)
            st.image(image, caption="Uploaded Certificate", use_container_width=True)
            st.code(text[:1000] + "..." if len(text) > 1000 else text)

    # --- NLP Analysis ---
    suspicious = detect_fake_keywords(text)
    missing = detect_missing_authentic_features(text)
    universities, degrees = extract_entities(text)
    degree_keywords_found = detect_degrees(text)
    score = calculate_fake_score(text)

    with analysis_col:
        st.subheader("Analysis Summary")

        col_score, col_info = st.columns([1, 2])
        with col_score:
            st.markdown("**Fake Score**")
            st.progress(score)

            if score >= 80:
                st.success(f"Score: {score}/100 – Likely Genuine")
            elif score >= 50:
                st.warning(f"Score: {score}/100 – Suspicious")
            else:
                st.error(f"Score: {score}/100 – Likely Fake")

        with col_info:
            st.markdown("**Key Observations**")
            st.metric("Suspicious Keywords", len(suspicious))
            st.metric("Missing Terms", len(missing))
            st.metric("University Names", len(universities))
            st.metric("Degree Mentions", len(degree_keywords_found))

        st.markdown("---")
        with st.expander("Fake Detection Details"):
            if suspicious:
                st.error("Suspicious keywords found:\n- " + "\n- ".join(suspicious))
            else:
                st.success("No suspicious keywords detected.")

            if missing:
                st.warning("Missing expected keywords:\n- " + "\n- ".join(missing))
            else:
                st.info("All essential terms present.")

        with st.expander("Extracted Entities"):
            if universities:
                st.success(f"Universities: {', '.join(universities)}")
            else:
                st.warning("No recognized universities found.")
            if degree_keywords_found:
                st.success(f"Degrees: {', '.join(degree_keywords_found)}")
            else:
                st.warning("No recognized degree types found.")

        st.markdown("---")
        st.caption("Analysis is heuristic-based and does not guarantee legal validity.")

else:
    st.info("Upload a certificate to begin analysis.")
