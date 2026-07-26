import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY", "").strip()
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing. Add a valid Groq API key to your .env file.")
if api_key.startswith("xai-"):
    raise RuntimeError("The current GROQ_API_KEY looks like an XAI key, not a Groq key. Replace it with a valid Groq API key.")

client = Groq(api_key=api_key)


def generate_image_prompt(product_name, description):
    system_prompt = (
        "You are an expert prompt engineer for AI image generation models "
        "used in e-commerce product photography. Given a product name and "
        "description, write ONE detailed image generation prompt (2-4 sentences) "
        "describing subject, styling/props, lighting, camera angle, background, "
        "and mood — suitable for a professional lifestyle product shot. "
        "Output ONLY the prompt, no preamble."
    )

    user_prompt = f"Product Name: {product_name}\nProduct Description: {description}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()