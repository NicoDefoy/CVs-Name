from flask import Flask, render_template, request
import random
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Initialiser l'application Flask
app = Flask(__name__)

# Listes élargies d'adjectifs et d'animaux
adjectives = [
    "Amazing", "Brilliant", "Clever", "Dazzling", "Excellent", "Fantastic",
    "Glorious", "Heroic", "Incredible", "Joyful", "Kind", "Luminous", "Magnificent",
    "Noble", "Outstanding", "Powerful", "Quick", "Radiant", "Spectacular", "Terrific",
    "Unique", "Vibrant", "Wonderful", "Zealous", "Adventurous", "Bold", "Creative",
    "Determined", "Energetic", "Fearless", "Generous", "Humble", "Innovative",
    "Jovial", "Keen", "Lively", "Motivated", "Nurturing", "Optimistic", "Passionate",
    "Resilient", "Strong", "Talented", "Upbeat", "Valiant", "Wise", "Bright", "Charming",
    "Friendly", "Gentle", "Harmonious", "Inspiring", "Joyous", "Loyal", "Peaceful",
    "Reliable", "Sparkling", "Steady", "Supportive", "Trustworthy", "Warm", "Zestful"
]

animals = [
    "Dog", "Cat", "Elephant", "Giraffe", "Lion", "Tiger", "Bear", "Eagle", "Shark", "Whale",
    "Dolphin", "Horse", "Penguin", "Panda", "Wolf", "Fox", "Rabbit", "Deer", "Zebra",
    "Leopard", "Cheetah", "Turtle", "Octopus", "Seal", "Otter", "Jellyfish", "Starfish",
    "Crab", "Lobster", "Seahorse", "Clownfish", "Koala", "Kangaroo", "Owl", "Hawk",
    "Sparrow", "Robin", "Parrot", "Pelican", "Swan", "Hummingbird", "Butterfly", "Beaver",
    "Squirrel", "Chimpanzee", "Gorilla", "Baboon", "Camel", "Buffalo", "Goat", "Sheep",
    "Pig", "Donkey", "Hedgehog", "Flamingo", "Raccoon", "Mole", "Mouse", "Antelope",
    "Orangutan", "Moose", "Peacock", "Turkey", "Dove", "Wombat", "Badger", "Porcupine"
]

# Initialiser les credentials Google Sheets à partir de la variable d'environnement
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON')), scopes=SCOPES
)
spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')  # ID de votre Google Sheet
sheet_range = "Noms!A1:A"  # Plage où sont stockés les noms dans la feuille

# Route pour l'index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Générer un nom aléatoire
        adjective = random.choice(adjectives)
        animal = random.choice(animals)
        generated_name = f"{adjective} {animal}"

        # Ajouter le nom dans Google Sheets
        ajouter_nom_dans_google_sheet(generated_name)

        return render_template('index.html', nom=generated_name)

    return render_template('index.html')

# Fonction pour ajouter le nom dans Google Sheets
def ajouter_nom_dans_google_sheet(nom):
    try:
        print("Débogage : Initialisation du service Google Sheets")
        service = build('sheets', 'v4', credentials=CREDS)
        sheet = service.spreadsheets()
        values = [[nom]]
        body = {
            'values': values
        }
        result = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        print(f"{result.get('updates').get('updatedCells')} cellule(s) ajoutée(s) dans Google Sheets.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du nom dans Google Sheets: {e}")

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
