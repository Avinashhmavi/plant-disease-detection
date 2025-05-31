# 🌿 Plant Disease Detector

An AI-powered web app that detects diseases in plant leaves or crops using advanced visual language models via OpenRouter and OpenAI APIs. Simply upload an image of a plant, and the app will analyze it, identify potential diseases, and highlight the affected region.

---

## 🚀 Features

- 🔍 **Plant Disease Detection**: Identifies visible signs of plant or crop diseases using AI.
- 📦 **Bounding Box Visualization**: Automatically highlights the affected region in the image.
- 📸 **Image Upload Support**: Accepts JPG, JPEG, and PNG image formats.
- 🧠 **Powered by OpenAI via OpenRouter**: Utilizes multimodal LLM (`qwen2.5-vl-72b-instruct`) to analyze visual and textual data.
- ⚙️ **Streamlit Interface**: Easy-to-use web interface with instant feedback.

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [OpenRouter](https://openrouter.ai/)
- [Pillow (PIL)](https://python-pillow.org/)

---

## 📂 Project Structure

├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── .streamlit/
└── secrets.toml        # API key configuration (not pushed to GitHub)

---

## ✅ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Avinashhmavi/plant-disease-detection.git
cd plant-disease-detector

2. Install Dependencies

pip install -r requirements.txt

3. Set Up API Key

Create a file at .streamlit/secrets.toml and add your OpenAI API key (via OpenRouter):

[openai]
api_key = "your-openrouter-api-key-here"

⚠️ Never commit secrets.toml to version control. Add it to .gitignore.

4. Run the App

streamlit run app.py


⸻

🌍 Deployment

You can deploy this app to Streamlit Cloud or any server supporting Python and Streamlit.

When deploying on Streamlit Cloud, ensure that secrets.toml is set through the web UI for secrets management.

⸻

📸 Example Usage

Upload an image like this:
	•	A leaf with possible disease spots

And get results like:
	•	✅ Disease Detected: Powdery Mildew
	•	📍 Bounding Box: [120, 95, 340, 280]

⸻

🛡️ Disclaimer

This tool is for educational and research purposes only. It is not a substitute for professional agricultural or botanical advice.

⸻

📄 License

MIT License © 2025 Avinash HM
