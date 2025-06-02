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

st.set_page_config(page_title="Plant / Crop Disease Detector", layout="centered")

# Create columns to display logos side by side
col1, col2 = st.columns(2)

# Display the two images side by side with reduced size
with col1:
    st.image("img1.jpeg", width=200)  # Adjusted width to make the logo smaller
with col2:
    st.image("img2.jpeg", width=800)  # Adjusted width to make the logo smaller

st.title("Neeev.ai - Plant Disease identification")
st.markdown("ਕਿਸੇ ਪੌਦੇ, ਪੱਤੇ ਜਾਂ ਫਸਲ ਦੀ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ, ਅਤੇ AI-ਸੰਚਾਲਿਤ ਬਿਮਾਰੀ ਦਾ ਪਤਾ ਲਗਾਓ।  (Upload an image of a plant, leaf, or crop, and get AI-powered disease detection.)")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_container_width=True)

    # Get file extension
    file_name = uploaded_file.name
    ext = file_name.split(".")[-1].lower()  # Get extension in lowercase

    # Map common extensions to supported Pillow formats
    if ext == "jpg":
        ext = "jpeg"
    elif ext == "png":
        ext = "png"
    else:
        ext = "jpeg"  # Default fallback

    # Convert image to base64 for prompt context
    buffered = io.BytesIO()
    image.save(buffered, format=ext.upper())  # Ensure uppercase format
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    with st.spinner("Analyzing image..."):
        try:
            # First: Ask model to detect disease and return bounding box
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

            # Display English result
            st.subheader("🔍 Analysis Result (English):")
            st.write(result)

            # Function to translate text to Punjabi using LLM
            def translate_to_punjabi_with_llm(text):
                if not text or len(text.strip()) == 0:
                    return "ਕੋਈ ਵੈਧ ਪਾਠ ਨਹੀਂ ਮਿਲਿਆ।"

                try:
                    trans_response = client.chat.completions.create(
                        model="qwen/qwen2.5-vl-72b-instruct:free",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a helpful assistant who translates English text into Punjabi."
                            },
                            {
                                "role": "user",
                                "content": f"Translate the following English text into Punjabi:\n\n{text}"
                            }
                        ],
                        max_tokens=300
                    )
                    return trans_response.choices[0].message.content.strip()
                except Exception as e:
                    return f"[ਪੰਜਾਬੀ ਅਨੁਵਾਦ ਉਪਲਬਧ ਨਹੀਂ] - {str(e)}"

            # Translate and display Punjabi result
            if result.strip():
                st.subheader("🔍 ਵਿਸ਼ਲੇਸ਼ਣ ਨਤੀਜਾ (ਪੰਜਾਬੀ):")
                punjabi_result = translate_to_punjabi_with_llm(result)
                st.write(punjabi_result)
            else:
                st.warning("No English result to translate.")

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
