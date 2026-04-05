import pdfplumber
import io
import fitz
from PIL import Image
import hashlib


def extract_text_from_pdf(file_bytes):
    text = ""

    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_text_and_images(file_bytes):
    text = extract_text_from_pdf(file_bytes)
    images = []
    seen_hashes = set()

    doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            # ❌ skip small images
            if len(image_bytes) < 15000:
                continue

            # ❌ skip duplicates
            hash_val = hashlib.md5(image_bytes).hexdigest()
            if hash_val in seen_hashes:
                continue
            seen_hashes.add(hash_val)

            try:
                img_pil = Image.open(io.BytesIO(image_bytes))

                # ❌ skip tiny dimensions
                if img_pil.width < 200 or img_pil.height < 200:
                    continue

                # ❌ skip weird ratios (banners)
                ratio = img_pil.width / img_pil.height
                if ratio > 5 or ratio < 0.2:
                    continue

            except:
                continue

            images.append(image_bytes)

    return text, images