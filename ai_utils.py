from openai import OpenAI
import json
import base64
import os

# 🔐 Load API key safely
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("❌ Missing OPENROUTER_API_KEY in environment variables")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")


def process_document(text, images=None):

    encoded_images = []
    if images:
        encoded_images = [encode_image(img) for img in images[:3]]

    prompt = f"""
You are a highly precise AI system designed to analyze structured technical inspection reports.

Your task is to extract structured insights and evaluate question-answer quality WITH CONTEXTUAL IMAGE ANALYSIS.

---

DOCUMENT ANALYSIS TASKS:

1. Identify all sections clearly.

2. Inside each section:
   - Extract all questions
   - Extract:
     - question
     - instruction (if present)
     - answer (if present)

3. For EACH question, evaluate STRICTLY:
   - Instruction Coverage (Full / Partial / Poor)
   - Detail Level (High / Medium / Low)
   - Missing Points (specific technical gaps)

4. IMAGE ANALYSIS:

You are also given images extracted from the document.

For EACH question:
- Compare the question + instruction + answer WITH the images

Then decide:
- Relevant / Not Relevant

IMPORTANT:
- Do NOT guess
- Ignore logos, decorative images

5. For EACH section:
   - Provide a concise summary

6. Provide overall summary:
   - strengths
   - weaknesses
   - gaps

---

OUTPUT FORMAT (STRICT JSON):

{{
  "sections": [
    {{
      "title": "Section name",
      "questions": [
        {{
          "question": "...",
          "evaluation": {{
            "coverage": "...",
            "detail": "...",
            "missing": "...",
            "image_relevance": "...",
            "image_reason": "..."
          }}
        }}
      ],
      "summary": "..."
    }}
  ],
  "overall_summary": "..."
}}

---

DOCUMENT:
{text[:8000]}
"""

    try:
        if encoded_images:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        *[
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{img}"
                                }
                            }
                            for img in encoded_images
                        ]
                    ]
                }],
                temperature=0.2
            )
        else:
            response = client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

        output_text = response.choices[0].message.content

        # clean markdown
        output_text = output_text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(output_text)
        except:
            return {"error": "Invalid JSON", "raw": output_text}

    except Exception as e:
        return {"error": "API failed", "details": str(e)}