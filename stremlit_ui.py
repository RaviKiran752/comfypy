import streamlit as st
import requests
import base64
from PIL import Image
import io

API_URL = "http://127.0.0.1:8000/generate"  

st.title(" AI Image Generator with ComfyUI")

positive_prompt = st.text_input("Positive Prompt", "A futuristic cyberpunk city")
negative_prompt = st.text_input("Negative Prompt", "low quality, bad composition")
seed = st.number_input("Seed", min_value=0, max_value=999999999, value=123456)
lora_strength = st.slider("LoRA Strength", 0.0, 1.5, 0.7, step=0.1)

generate_button = st.button("Generate Image")

if generate_button:
    with st.spinner("Generating..."):
        payload = {
            "positive_prompt": positive_prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "lora_strength": lora_strength,
        }
        
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 200:
            images = response.json().get("images", [])
            for img_data in images:
                image_bytes = base64.b64decode(img_data)
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Generated Image", use_column_width=True)
        else:
            st.error("Failed to generate image. Please check the backend.")
