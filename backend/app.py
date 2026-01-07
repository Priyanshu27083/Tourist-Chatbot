from flask import Flask, request, jsonify
from flask_cors import CORS
from model import predict_category
from response_gen import generate_reply
import google.generativeai as genai
import os
from dotenv import load_dotenv
import random
import requests

# 🌿 Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# 🤖 Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # stable model

# 🟢 Greeting detector
def is_greeting(text):
    greetings = ["hi", "hello", "hey", "namaste", "good morning", "good evening", "good afternoon"]
    text = text.lower().strip()
    return any(text.startswith(g) or text == g for g in greetings)

# ✨ Randomized greeting response
def greeting_reply():
    options = [
        "Namaste! I’m TourMate — your travel buddy for exploring India!",
        "Hey there! Ready to plan your next Indian adventure?",
        "Hello traveler! Where would you like to explore today?",
        "Hi wanderer! Need help discovering amazing places in India?",
        "Welcome back, explorer! Let’s make your next trip unforgettable.",
    ]
    return random.choice(options)


# 🌦️ WEATHER HELPERS
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return None

    temp = response["main"]["temp"]
    desc = response["weather"][0]["description"].title()
    humidity = response["main"]["humidity"]

    return {"temp": temp, "desc": desc, "humidity": humidity}


def generate_weather_reply(place, weather):
    temp = weather["temp"]
    desc = weather["desc"]
    humidity = weather["humidity"]

    # Rainy
    if "rain" in desc.lower() or humidity > 75:
        return (
            f"It’s currently {desc.lower()} in {place} with {temp}°C 🌧\n"
            f"- Consider indoor attractions today.\n"
            f"- Roads might be slippery; avoid biking.\n"
            f"- Carry an umbrella or raincoat.\n"
        )

    # Hot
    if temp > 32:
        return (
            f"{place} is quite hot right now at {temp}°C ☀️\n"
            f"- Visit outdoor places early morning or after 5 PM.\n"
            f"- Stay hydrated and use sunscreen.\n"
        )

    # Cold
    if temp < 18:
        return (
            f"It’s chilly in {place} today at {temp}°C ❄️\n"
            f"- Carry a jacket.\n"
            f"- Evenings are great for markets and hot snacks.\n"
        )

    # Pleasant
    return (
        f"The weather in {place} looks pleasant — {temp}°C, {desc.lower()} ☀️\n"
        f"- Perfect for sightseeing and outdoor activities.\n"
    )


# --------------------------------------------------------
# 🚀 MAIN CHAT ENDPOINT
# --------------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    # Step 0️⃣ — Greeting
    if is_greeting(user_message):
        reply = greeting_reply()
        return jsonify({"reply": reply, "category": "greeting"})

    # Step 1️⃣ — Predict using trained ML model
    category = predict_category(user_message)

    # Step 2️⃣ — Special branch: WEATHER
    if category == "weather":
        from response_gen import extract_place
        place = extract_place(user_message)
        if place:
            weather = get_weather(place)
            if weather:
                reply = generate_weather_reply(place, weather)
                return jsonify({"reply": reply, "category": "weather"})
            else:
                return jsonify({
                    "reply": f"Sorry, I couldn't fetch the weather details for {place}.",
                    "category": "weather_error"
                })
        else:
            return jsonify({
                "reply": "Please specify a city in India to get weather updates.",
                "category": "weather_missing_place"
            })

    # Step 3️⃣ — If ML is confident → normal trained reply
    if category:
        print(f"[Model] Confident: using trained model for '{category}'")
        reply = generate_reply(user_message, category)
        return jsonify({"reply": reply, "category": "trained_model"})

    # Step 4️⃣ — Gemini fallback
    print("[Gemini] Model unsure — using Gemini fallback")

    prompt = f"""
    You are TourMate, a friendly Indian travel and tourism assistant.

    The user asked: "{user_message}".

    Respond ONLY if it is related to:
    - Indian travel or trip planning
    - tourist places, destinations, or attractions
    - Indian food or cuisine
    - routes, transport, or travel tips in India

    If the message is NOT related to Indian tourism/travel/food, reply exactly:
    "Sorry, I can only answer travel or tourism related questions about India 🇮🇳."

    Otherwise, give a short, friendly, accurate answer.
    """

    try:
        response = gemini_model.generate_content(prompt)
        reply = response.text
        return jsonify({"reply": reply, "category": "gemini"})
    except Exception as e:
        print("Gemini Error:", e)
        return jsonify({"reply": "Sorry, I couldn’t connect to Gemini right now.", "category": "error"})


# --------------------------------------------------------
# 🚀 RUN SERVER
# --------------------------------------------------------
if __name__ == "__main__":
    print("🚀 TourMate backend running at http://127.0.0.1:5000")
    app.run(debug=True)
