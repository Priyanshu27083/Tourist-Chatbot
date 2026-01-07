import random
import re

best_time_visit = {
    "Goa": "November to February",
    "Hyderabad": "October to February",
    "Delhi": "October to March",
    "Mumbai": "November to February",
    "Kerala": "September to March",
    "Chennai": "November to February",
    "Bangalore": "October to February",
    "Kolkata": "October to February",
    "Jaipur": "November to February",
    "Agra": "November to February",
    "Manali": "October to February",
    "Shimla": "October to February",
    "Rajasthan": "October to March",
    "Uttarakhand": "March to June",
    "Ladakh": "May to September"
}

def get_best_time_static(place):
    return best_time_visit.get(place, None)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = text.replace('foods', 'food')
    text = text.replace('places', 'place')
    text = text.strip()
    return text

def extract_place(text):
    """Detect Indian location names from user input."""
    text = text.lower()
    places = [
        "delhi", "mumbai", "goa", "kerala", "hyderabad", "kolkata",
        "chennai", "bengaluru", "bangalore", "agra", "jaipur", "manali",
        "shimla", "rajasthan", "punjab", "gujarat", "assam", "sikkim",
        "tamil nadu", "uttarakhand", "ladakh", "himachal pradesh", "odisha",
        "bihar", "jharkhand", "west bengal", "uttar pradesh", "madhya pradesh",
        "chhattisgarh", "goa", "tripura", "meghalaya", "nagaland", "manipur",
        "mizoram", "arunachal pradesh", "telangana", "andhra pradesh", "punjab",
        "haryana", "rajasthan", "maharashtra", "sikkim", "kerala", "tamil nadu", "karnataka", "andaman and nicobar islands", "dadra and nagar haveli", "daman and diu", "puducherry"
    ]
    for p in places:
        if p in text:
            return p.title()
    return None

def generate_reply(prompt, category):
    place = extract_place(prompt)
    key_place = place if place else "India"

    if category == "places":
        responses = [
            f"{key_place} has some wonderful tourist spots — from historic forts to peaceful natural retreats.",
            f"You should explore {key_place}’s local highlights. Would you like nature spots or cultural places?",
            f"There’s so much to see in {key_place}! Every region has its charm — forts, temples, and cozy hill stations.",
        ]

    elif category == "food":
        responses = [
            f"The food in {key_place} will truly impress you — try regional specialties like biryani, thali, or street snacks!",
            f"You’ll love the cuisine in {key_place}. From spicy curries to sweets like jalebi or rasgulla — it’s a treat!",
            f"Craving something authentic? In {key_place}, dishes like dosa, chaat, and masala chai are must-tries!",
        ]

    elif category == "tips":
        responses = [
            f"If you’re visiting {key_place}, pack light cottons in summer and keep sunscreen handy!",
            f"Travel tip — in {key_place}, mornings are best for sightseeing before it gets crowded or hot.",
            f"Smart move asking ahead! For {key_place}, plan around the local season — winter is usually perfect for exploring.",
        ]

    elif category == "transport":
        responses = [
            f"To travel within {key_place}, use local transport apps or metros if available — easy and affordable!",
            f"For getting around {key_place}, autos and buses are common — or book cabs using Ola or Uber.",
            f"Heading to {key_place}? Trains are great for longer routes, and local buses help you explore the city easily.",
        ]

    else:
        responses = [
            f"I can share info about Indian places, food, transport, or travel tips — where would you like to start?",
            f"Hmm, I didn’t catch that fully. Try asking about a place, food, or how to travel somewhere in India!",
        ]

    return random.choice(responses)
