from flask import Flask, render_template, request
import cv2
import numpy as np
import os
from groq import Groq
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Debug print (you can remove later)
print("Loaded GROQ API KEY:", GROQ_API_KEY)

client = Groq(api_key=GROQ_API_KEY)

app = Flask(__name__)

# Uploads folder inside static
app.config['UPLOAD_FOLDER'] = os.path.join("static", "uploads")

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def detect_skin_tone(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "Unknown"

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    h, w, _ = img.shape
    center = img[h//3:2*h//3, w//3:2*w//3]
    avg_color = np.mean(center, axis=(0, 1))
    brightness = np.mean(avg_color)

    if brightness > 200:
        return "Fair"
    elif brightness > 150:
        return "Medium"
    elif brightness > 100:
        return "Olive"
    else:
        return "Deep"


def get_ai_recommendation(skin_tone, gender):
    prompt = f"""
You are a fashion expert. Give personalized fashion advice for a {gender} person with {skin_tone} skin tone.
Suggest:
- Best colors
- Outfit types
- Accessories
- Hairstyle
Explain in simple and friendly language.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful fashion stylist."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/result", methods=["POST"])
def result():
    file = request.files["image"]
    gender = request.form.get("gender", "Not specified")

    if not file or file.filename == "":
        return render_template("home.html")

    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    skin_tone = detect_skin_tone(path)

    ai_text = get_ai_recommendation(skin_tone, gender)

    return render_template(
        "result.html",
        skin_tone=skin_tone,
        gender=gender,
        ai_text=ai_text
    )


if __name__ == "__main__":
    app.run(debug=True)