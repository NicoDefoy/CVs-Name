from flask import Flask, render_template, request
import random
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Configuration de Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS = Credentials.from_service_account_file("Noms_CV/client_secret.json", scopes=SCOPES)
client = gspread.authorize(CREDS)

# Ouvrir le Google Sheet
sheet = client.open("Flinter's Name").sheet1

# Liste complète d'adjectifs
adjectives = [
    "Amazing", "Brilliant", "Clever", "Dazzling", "Excellent", "Fantastic",
    "Glorious", "Heroic", "Incredible", "Joyful", "Kind", "Luminous", "Magnificent",
    "Noble", "Outstanding", "Powerful", "Quick", "Radiant", "Spectacular", "Terrific",
    "Unique", "Vibrant", "Wonderful", "Xenial", "Youthful", "Zealous", "Adventurous",
    "Bold", "Creative", "Determined", "Energetic", "Fearless", "Generous", "Humble",
    "Innovative", "Jovial", "Keen", "Lively", "Motivated", "Nurturing", "Optimistic",
    "Passionate", "Quirky", "Resilient", "Strong", "Talented", "Upbeat", "Valiant", "Wise"
]

# Liste complète d'animaux
animals = [
    "Lion", "Tiger", "Bear", "Eagle", "Shark", "Elephant", "Giraffe", "Dolphin", "Whale",
    "Penguin", "Kangaroo", "Panda", "Wolf", "Fox", "Rabbit", "Deer", "Horse", "Zebra",
    "Leopard", "Cheetah", "Turtle", "Octopus", "Seal", "Otter", "Jellyfish", "Starfish",
    "Crab", "Lobster", "Seahorse", "Clownfish"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Générer un nom aléatoire
        adjective = random.choice(adjectives)
        animal = random.choice(animals)
        generated_name = f"{adjective} {animal}"

        # Enregistrer dans Google Sheet
        sheet.append_row([generated_name])

        return render_template('index.html', nom=generated_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
