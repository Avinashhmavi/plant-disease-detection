import streamlit as st
from openai import OpenAI
from PIL import Image, ImageDraw
import base64
import io
import re  # For parsing coordinates from the model's response

# Initialize OpenAI client with OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1", 
    api_key=st.secrets["openai"]["api_key"]
)

st.set_page_config(page_title="Plant Disease Detector", layout="centered")

st.title("🪴 Plant / Crop Disease Detection 🌾")
st.markdown("Upload an image of a plant, leaf, or crop, and get AI-powered disease detection.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Get file extension
    file_name = uploaded_file.name
    ext = file_name.split(".")[-1].upper()

    if ext not in ["JPEG", "JPG", "PNG"]:
        ext = "JPEG"

    # Convert image to base64 for prompt context
    buffered = io.BytesIO()
    image.save(buffered, format=ext)
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    with st.spinner("Analyzing image..."):
        try:
            # Update prompt to request bounding box coordinates
            response = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://plant-disease-detector.streamlit.app", 
                    "X-Title": "Plant Disease Detector"
                },
                model="qwen/qwen2.5-vl-72b-instruct:free",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "You are a plant disease expert assistant. If this image contains a plant, tree, or crop "
                                    "and shows signs of disease, describe the disease and identify the affected area. Provide "
                                    "the bounding box coordinates [x1, y1, x2, y2] around the diseased region. If no disease "
                                    "is visible, say so clearly. Only respond if the image is related to plants or crops."
                                )
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_b64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )

            result = response.choices[0].message.content.strip()
            st.subheader("🔍 Analysis Result:")
            st.write(result)

            # Extract bounding box coordinates from the response
            bbox_pattern = r"\[(\d+), (\d+), (\d+), (\d+)\]"
            match = re.search(bbox_pattern, result)

            if match:
                x1, y1, x2, y2 = map(int, match.groups())
                st.write(f"Bounding Box Coordinates: [{x1}, {y1}, {x2}, {y2}]")

                # Draw bounding box on the image
                draw = ImageDraw.Draw(image)
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
                st.image(image, caption="Disease Area Highlighted", use_container_width=True)
            else:
                st.warning("No bounding box coordinates found in the model's response.")
                st.image(image, caption="Disease Area Highlighted", use_container_width=True)

        except Exception as e:
            st.error(f"Error occurred during analysis: {e}")
