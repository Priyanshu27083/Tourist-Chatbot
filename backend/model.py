from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import nltk
import numpy as np
import re

nltk.download("stopwords", quiet=True)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = text.replace('foods', 'food')
    text = text.replace('greetings', 'greeting')
    text = text.replace('transportation', 'transport')
    text = text.replace('weathers', 'weather')
    text = text.replace('tipsy', 'tips')
    text = text.replace('places', 'place')
    text = text.strip()
    return text

data = [

    # 🟢 GREETING
    ("hello", "greeting"),
    ("hi", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),
    ("namaste", "greeting"),
    ("how are you", "greeting"),
    ("what's up", "greeting"),
    ("good to see you", "greeting"),
    ("greetings", "greeting"),
    ("hey there", "greeting"),
    ("yo", "greeting"),
    ("hi tourmate", "greeting"),
    ("hello there", "greeting"),
    ("good afternoon", "greeting"),
    ("hi, how are you doing", "greeting"),
    ("nice to meet you", "greeting"),
    ("what’s new", "greeting"),
    ("hi buddy", "greeting"),
    ("hey tourmate", "greeting"),
    ("hello friend", "greeting"),
    ("hi assistant", "greeting"),
    ("hey how’s it going", "greeting"),
    ("long time no see", "greeting"),
    ("good day", "greeting"),
    ("how are things", "greeting"),
    ("how have you been", "greeting"),
    ("hello mate", "greeting"),
    ("hey! need help", "greeting"),
    ("hi! can you help me", "greeting"),
    ("hello! what's happening", "greeting"),
    ("hey there tour guide", "greeting"),
    ("hi! I have a question", "greeting"),
    ("hello! can you assist", "greeting"),
    ("hey! I’m planning a trip", "greeting"),
    ("hello travel assistant", "greeting"),
    ("good morning tourmate", "greeting"),
    ("hi explorer", "greeting"),
    ("hey! what can you do", "greeting"),
    ("hello chatbot", "greeting"),
    ("hi! need guidance", "greeting"),
    ("hey, I need info", "greeting"),
    ("hello, tell me something", "greeting"),
    ("hey, how’s your day", "greeting"),
    ("hi, I’m back", "greeting"),
    ("hello, I need help", "greeting"),

    # 🟡 PLACES
    ("famous places to visit in Delhi", "places"),
    ("top attractions in Mumbai", "places"),
    ("best beaches in Goa", "places"),
    ("hill stations in Himachal", "places"),
    ("temples in Tamil Nadu", "places"),
    ("tourist spots in Rajasthan", "places"),
    ("heritage sites in Hyderabad", "places"),
    ("wildlife sanctuaries in Kerala", "places"),
    ("places to see in Kolkata", "places"),
    ("must visit places in India", "places"),
    ("top places to travel in India", "places"),
    ("tourist places near Chennai", "places"),
    ("weekend getaways from Bangalore", "places"),
    ("romantic places in India", "places"),
    ("famous forts in Maharashtra", "places"),
    ("best places to visit in Pune", "places"),
    ("famous waterfalls in India", "places"),
    ("adventure spots in Uttarakhand", "places"),
    ("popular tourist destinations", "places"),
    ("best places for family trips", "places"),
    ("tourist attractions in Mysore", "places"),
    ("historical monuments in Delhi", "places"),
    ("places to explore in Gujarat", "places"),
    ("best places to travel in Karnataka", "places"),
    ("hill stations near Pune", "places"),
    ("beautiful places in Assam", "places"),
    ("top tourist places in Sikkim", "places"),
    ("lake destinations in India", "places"),
    ("heritage places in Jaipur", "places"),
    ("eco tourism spots in India", "places"),
    ("famous caves in India", "places"),
    ("wildlife destinations in Madhya Pradesh", "places"),
    ("beach destinations near Mumbai", "places"),
    ("famous gardens in Bangalore", "places"),
    ("best places to visit in Telangana", "places"),
    ("cultural places in Tamil Nadu", "places"),
    ("must-see places in Varanasi", "places"),
    ("tourist places near Hyderabad", "places"),
    ("nature places in Kerala", "places"),
    ("hill stations near Hyderabad", "places"),
    ("best scenic spots in Coorg", "places"),
    ("famous temples in Karnataka", "places"),
    ("historical sites in Gujarat", "places"),
    ("weekend trips from Delhi", "places"),
    ("best adventure places in India", "places"),
    ("famous trekking places in India", "places"),
    ("top viewpoints in India", "places"),
    ("places to visit in Ladakh", "places"),
    ("hidden gems in India", "places"),
    ("best places for photography in India", "places"),
    ("must visit beaches in India", "places"),

    # 🔴 FOOD
    ("what food should I try in Hyderabad", "food"),
    ("famous dishes of Punjab", "food"),
    ("street food in Delhi", "food"),
    ("traditional food of Gujarat", "food"),
    ("popular snacks in Mumbai", "food"),
    ("famous sweets in Kolkata", "food"),
    ("best food in South India", "food"),
    ("what can I eat in Kerala", "food"),
    ("local food to eat in Jaipur", "food"),
    ("Hyderabadi biryani specialty", "food"),
    ("what are the best foods in Hyderabad", "food"),
    ("must try dishes in Hyderabad", "food"),
    ("top street food in India", "food"),
    ("what should I eat in Chennai", "food"),
    ("best restaurants in Delhi", "food"),
    ("authentic food in Rajasthan", "food"),
    ("famous desserts in India", "food"),
    ("signature dishes of Bangalore", "food"),
    ("best north Indian food", "food"),
    ("south Indian breakfast dishes", "food"),
    ("best seafood in Goa", "food"),
    ("what to eat in Mumbai", "food"),
    ("famous vegetarian dishes in India", "food"),
    ("top breakfast foods in India", "food"),
    ("best street snacks in Hyderabad", "food"),
    ("popular sweets in South India", "food"),
    ("famous biryanis in India", "food"),
    ("what to try in Bangalore restaurants", "food"),
    ("best dhabas on Indian highways", "food"),
    ("famous chaats in India", "food"),
    ("best masala dosa places", "food"),
    ("top Indian thali meals", "food"),
    ("popular Bengali dishes", "food"),
    ("famous Gujarati snacks", "food"),
    ("best Rajasthani food", "food"),
    ("famous South Indian tiffins", "food"),
    ("popular north Indian curries", "food"),
    ("street food near India Gate", "food"),
    ("best restaurants in Hyderabad", "food"),
    ("top spicy foods in India", "food"),
    ("famous laddus in India", "food"),
    ("best chai places in India", "food"),

    # 🔵 TIPS
    ("best time to visit Kerala", "tips"),
    ("is summer good for Rajasthan", "tips"),
    ("how to travel cheap in India", "tips"),
    ("how to plan a budget trip", "tips"),
    ("packing advice for India trip", "tips"),
    ("travel tips for monsoon season", "tips"),
    ("how to stay safe while traveling", "tips"),
    ("how to avoid crowds while sightseeing", "tips"),
    ("what clothes to pack for Goa trip", "tips"),
    ("how to prepare for trekking", "tips"),
    ("how to stay healthy while traveling", "tips"),
    ("best time to travel to North India", "tips"),
    ("how to book cheap hotels", "tips"),
    ("what to carry on a long trip", "tips"),
    ("tips for solo travelers", "tips"),
    ("is monsoon a good time for Kerala", "tips"),
    ("how to plan India tour", "tips"),
    ("how to avoid travel scams", "tips"),
    ("how to travel safely at night", "tips"),
    ("best season to visit Himalayas", "tips"),
    ("how to save money on flights", "tips"),
    ("what to pack for a hill station", "tips"),
    ("summer travel safety tips", "tips"),
    ("monsoon travel precautions", "tips"),
    ("important things to pack for trekking", "tips"),
    ("how to stay hydrated while traveling", "tips"),
    ("is winter good for Ladakh", "tips"),
    ("best time to visit beaches in India", "tips"),
    ("how to book train tickets quickly", "tips"),
    ("tips for safe solo travel", "tips"),
    ("budget tips for Goa trip", "tips"),
    ("best time to visit tourist places", "tips"),
    ("how to plan a weekend trip", "tips"),
    ("things to avoid during monsoon travel", "tips"),
    ("travel safety for families", "tips"),

    # 🟣 TRANSPORT
    ("how to go from Delhi to Agra", "transport"),
    ("is metro available in Hyderabad", "transport"),
    ("how to book train tickets", "transport"),
    ("best way to reach Jaipur from Delhi", "transport"),
    ("local transport in Mumbai", "transport"),
    ("bus services in Bangalore", "transport"),
    ("taxi options in Chennai", "transport"),
    ("flight to Goa", "transport"),
    ("train from Mumbai to Pune", "transport"),
    ("how to reach Manali from Delhi", "transport"),
    ("public transport in Kolkata", "transport"),
    ("cab services in Delhi", "transport"),
    ("cheapest way to travel in India", "transport"),
    ("how to travel between cities in India", "transport"),
    ("is Uber available in India", "transport"),
    ("metro timings in Bangalore", "transport"),
    ("best bus routes in South India", "transport"),
    ("cheapest flight options to Kerala", "transport"),
    ("how to reach Goa from Hyderabad", "transport"),
    ("local trains in Mumbai information", "transport"),
    ("best way to travel inside Bangalore", "transport"),
    ("metro routes in Delhi", "transport"),
    ("how to reach Ooty from Chennai", "transport"),
    ("cab options in Hyderabad", "transport"),
    ("bus timings in Telangana", "transport"),
    ("train timings in India", "transport"),
    ("how to book tatkal tickets", "transport"),
    ("transport facilities in Goa", "transport"),
    ("travel options from Mumbai airport", "transport"),
    ("best transport for Ladakh trip", "transport"),

    # 🔵 WEATHER
    ("weather in Mumbai", "weather"),
    ("current weather in Delhi", "weather"),
    ("is it raining in Goa", "weather"),
    ("temperature in Hyderabad", "weather"),
    ("climate in Kerala", "weather"),
    ("forecast for Chennai", "weather"),
    ("is it hot in Rajasthan", "weather"),
    ("is it cold in Shimla", "weather"),
    ("how is the weather there", "weather"),
    ("today weather in Bangalore", "weather"),
    ("weather in Hyderabad", "weather"),
    ("current weather in Hyderabad", "weather"),
    ("today weather in Hyderabad", "weather"),
    ("is it raining in Hyderabad", "weather"),
    ("temperature in Hyderabad", "weather"),
    ("forecast for Hyderabad", "weather"),
    ("is it hot in Hyderabad", "weather"),
    ("is it cold in Hyderabad", "weather"),
    ("climate in Hyderabad", "weather"),
]

train_texts, train_labels = zip(*data)
train_texts = [clean_text(t) for t in train_texts]

stop_words = stopwords.words("english")
vectorizer = TfidfVectorizer(stop_words=stop_words)
X_train = vectorizer.fit_transform(train_texts)

clf = LogisticRegression(max_iter=500)
clf.fit(X_train, train_labels)

# Convert texts
cleaned_texts = [clean_text(t) for t in train_texts]

# Split
X_train_text, X_test_text, y_train, y_test = train_test_split(
    cleaned_texts, train_labels, test_size=0.2, random_state=42
)

# Vectorize using ONLY training data
X_train_vec = vectorizer.fit_transform(X_train_text)
X_test_vec  = vectorizer.transform(X_test_text)

# Train the classifier
clf = LogisticRegression(max_iter=500)
clf.fit(X_train_vec, y_train)

# Predict on test
y_pred = clf.predict(X_test_vec)

# Accuracy
print("Model Accuracy:", accuracy_score(y_test, y_pred))

def predict_category(prompt):
    """Predict category, or return None if not confident."""
    prompt = clean_text(prompt)
    X_test = vectorizer.transform([prompt])
    probs = clf.predict_proba(X_test)[0]
    max_prob = np.max(probs)
    label = clf.classes_[np.argmax(probs)]

    # Confidence threshold
    if max_prob < 0.4:  # lowered a bit to avoid unnecessary Gemini fallback
        return None
    return label