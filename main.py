from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from pdf_utils import extract_text_and_images
from ai_utils import process_document
app = FastAPI()

# 🌍 CORS (allow all for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route (important for Render)
@app.get("/")
def root():
    return {"message": "API is running 🚀"}

@app.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):
    contents = await file.read()

    print("📄 File received")

    text, images = extract_text_and_images(contents)

    # filter images
    filtered_images = [img for img in images if len(img) > 15000][:5]

    print(f"Text length: {len(text)}")
    print(f"Images used: {len(filtered_images)}")

    result = process_document(text, filtered_images)

    return result

@app.get("/test")
def test():
    return {"message": "backend working"}