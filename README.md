
---

# 📁 BACKEND README (ParseSmart_backend)

```md
# 🤖 ParseSmart – AI PDF Analyzer (Backend)

This is the backend service for ParseSmart, an AI-powered PDF analysis system.  
It extracts text and images from PDFs and uses an LLM to generate structured insights.

---

## 🚀 Live API

👉 https://parsesmart-backend.onrender.com/

---

## 🧠 Features

- 📄 PDF text extraction
- 🖼️ Image extraction & filtering
- 🧩 Section identification
- ❓ Question-answer evaluation
- 📊 Structured JSON output
- ⚡ FastAPI-based API

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Language:** Python
- **PDF Processing:** pdfplumber, PyMuPDF
- **Image Handling:** Pillow
- **AI Integration:** OpenRouter (GPT-4o-mini)
- **Deployment:** Render

---

## ⚙️ Setup (Local)

```bash
git clone https://github.com/Isaac1740/ParseSmart_backend.git
cd ParseSmart_backend
pip install -r requirements.txt
uvicorn main:app --reload
