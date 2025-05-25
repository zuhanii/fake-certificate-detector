# fake-certificate-detector

# 🎓 Fake Certificate Detector

A smart tool to detect potential forgeries in academic certificates and degrees using OCR, NLP, and heuristic analysis.

## 🔍 Overview

This Streamlit-based web application allows users to upload certificate images or PDFs and uses intelligent algorithms to:
- Extract text using OCR (Tesseract)
- Analyze key entities like universities and degree names using spaCy
- Flag suspicious or missing terms commonly seen in genuine certificates
- Calculate a "Fake Score" to estimate authenticity likelihood

## 💡 Features

- 🖼️ Supports image (`.jpg`, `.png`) and PDF uploads
- 📄 Text extraction using Tesseract and PyMuPDF
- 🧠 Named Entity Recognition (NER) for universities and degrees
- 🚩 Detection of suspicious keywords and missing authentic phrases
- 📊 Visual "Fake Score Meter" for quick decision support
- Streamlined and intuitive user interface with dual-column layout

## ⚙️ Tech Stack

- Python 3
- [Streamlit](https://streamlit.io/)
- [pytesseract](https://pypi.org/project/pytesseract/)
- [spaCy](https://spacy.io/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Pillow](https://pillow.readthedocs.io/)

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fake-certificate-detector.git
cd fake-certificate-detector
