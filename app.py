import streamlit as st
from PIL import Image
import io
import openai  # if you're using OpenAI models

st.title("Image Content Validator")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert to byte stream for sending to AI model
    image_bytes = uploaded_file.read()
    
    # Proceed with analysis
    # (You can use GPT-4-Vision, or another model)

import base64

# Convert image to base64
base64_image = base64.b64encode(image_bytes).decode("utf-8")

response = openai.ChatCompletion.create(
    model="gpt-4-vision-preview",
    messages=[
        {"role": "user", "content": [
            {"type": "text", "text": "Is the content in this image appropriate or correct based on general knowledge?"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
        ]}
    ],
    max_tokens=500
)

st.write("AI Analysis:")
st.write(response.choices[0].message["content"])

