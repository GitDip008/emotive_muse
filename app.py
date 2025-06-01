import os
import requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
HUGGING_FACE_MODEL_ID = os.getenv("HUGGING_FACE_MODEL_ID")

if not HUGGING_FACE_API_KEY or not HUGGING_FACE_MODEL_ID:
    raise RuntimeError("HUGGING_FACE_API_KEY or HUGGING_FACE_MODEL_ID missing from .env")

HF_INFERENCE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGING_FACE_MODEL_ID}"
HEADERS = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}",
    "Content-Type": "application/json"
}

app = Flask(__name__)

mood_data = {
    "happy": {
        "colors": ["#FFF700", "#FFC300", "#FF5733"],
        "image": "https://i.pinimg.com/736x/e8/99/5e/e8995e9eadb16677afd3115863e8f095.jpg",
        "youtube": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"
    },
    "sad": {
        "colors": ["#3B5998", "#223366", "#111133"],
        "image": "https://i.pinimg.com/736x/bd/a8/cd/bda8cdd7057a326182671ade90642a55.jpg",
        "youtube": "https://www.youtube.com/watch?v=4N3N1MlvVc4"
    },
    "calm": {
        "colors": ["#A3E4D7", "#76D7C4", "#48C9B0"],
        "image": "https://i.pinimg.com/736x/11/2c/db/112cdb6c2d0fd8d9b998ddb5c4b0f4d2.jpg",
        "youtube": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"
    },
    "angry": {
        "colors": ["#FF0000", "#990000", "#660000"],
        "image": "https://i.pinimg.com/736x/61/18/c4/6118c4834b65394bb846896a76d848df.jpg",
        "youtube": "https://www.youtube.com/watch?v=X2WH8mHJnhM"
    }
}

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Emotive Muse{% if emotion %} - {{ emotion | capitalize }}{% endif %}</title>
</head>
<body style="background-color: {{ bg_color }}; color: #222; font-family: Arial, sans-serif; padding: 20px;">
  <h2>Emotive Muse</h2>
  <p>Type one emotion from these: <strong>happy, sad, calm, angry</strong></p>
  <form method="POST">
    <input name="emotion" type="text" required />
    <button type="submit">Generate</button>
  </form>

  {% if result %}
    <h3>AI Generated Passage:</h3>
    <p>{{ result.passage }}</p>

    <h3>AI Generated Quote:</h3>
    <p>{{ result.quote }}</p>

    {% if result.song %}
      <h3>AI Suggested Song:</h3>
      <p>{{ result.song }}</p>
    {% endif %}

    {% if result.youtube %}
      <h3>Predefined Song Link:</h3>
      <a href="{{ result.youtube }}" target="_blank">Listen on YouTube</a>
    {% endif %}

    {% if result.image %}
      <h3>Suggested Image according to "{{ emotion }}":</h3>
      <img src="{{ result.image }}" alt="{{ emotion }} Mood Image" />
    {% endif %}

    {% if result.colors %}
      <h3>Predefined Colors for "{{ emotion }}":</h3>
      <div style="display:flex; gap:10px;">
        {% for color in result.colors %}
          <div style="width:50px; height:50px; background:{{ color }};"></div>
        {% endfor %}
      </div>
    {% endif %}
  {% endif %}
</body>
</html>
"""

def query_hugging_face_model(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 250,
            "temperature": 0.7,
            "do_sample": True,
            "return_full_text": False
        }
    }
    try:
        response = requests.post(HF_INFERENCE_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and result:
            return result[0].get("generated_text", "").strip()
        return ""
    except requests.exceptions.RequestException as e:
        print(f"Error calling Hugging Face API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"HF API detailed error: {e.response.text}")
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    bg_color = "#FFFFFF"
    emotion = ""

    if request.method == "POST":
        emotion = request.form.get("emotion", "").lower()

        if emotion not in mood_data:
            result = {
                "passage": "Unsupported emotion.",
                "quote": "Try one of: happy, sad, calm, angry.",
                "song": "",
                "image": "",
                "colors": [],
                "youtube": ""
            }
        else:
            prompt = f"""Give a short inspirational passage of 4 to 5 lines for someone feeling {emotion}. Passage MUST be generated.
Give a quote of a famous person about {emotion}. Must generate at least one.
Suggest a song title with {emotion} from youtube. Must generate at least one.
Suggest a color hex code that best matches the {emotion}. Must generate at least one.

Please format your response clearly, for example:
Passage: [Your passage here]
Quote: "[Your quote here]" - [Author]
Youtube: [Song Title]
Color: #XXXXXX

Must follow the exact format given here and generate at least one response for each category.
"""
            generated_text = query_hugging_face_model(prompt)

            # Defaults
            passage = "No passage generated"
            quote = "No quote generated."
            youtube_title = ""
            color_code = None

            if generated_text:
                lines = generated_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.lower().startswith("passage:"):
                        passage = line[8:].strip()
                    elif line.lower().startswith("quote:"):
                        quote = line[6:].strip()
                    elif line.lower().startswith("youtube:"):
                        youtube_title = line[8:].strip()
                    elif line.lower().startswith("color:"):
                        color_code = line[6:].strip()

            if not color_code:
                color_code = mood_data[emotion]["colors"][0]

            bg_color = color_code

            result = {
                "passage": passage,
                "quote": quote,
                "song": youtube_title,
                "image": mood_data[emotion]["image"],
                "colors": mood_data[emotion]["colors"],
                "youtube": mood_data[emotion]["youtube"]
            }

    return render_template_string(HTML, result=result, bg_color=bg_color, emotion=emotion)


if __name__ == "__main__":
    app.run(debug=True)