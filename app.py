from flask import Flask, render_template, request
import random
import os
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Initialiser l'application Flask
app = Flask(__name__)

# Listes d'adjectifs et d'animaux (version étendue)
adjectives = [
    "Amazing", "Brilliant", "Clever", "Dazzling", "Excellent", "Fantastic",
    "Glorious", "Heroic", "Incredible", "Joyful", "Kind", "Luminous", "Magnificent",
    "Noble", "Outstanding", "Powerful", "Quick", "Radiant", "Spectacular", "Terrific",
    "Unique", "Vibrant", "Wonderful", "Xenial", "Youthful", "Zealous", "Adventurous",
    "Bold", "Creative", "Determined", "Energetic", "Fearless", "Generous", "Humble",
    "Innovative", "Jovial", "Keen", "Lively", "Motivated", "Nurturing", "Optimistic",
    "Passionate", "Quirky", "Resilient", "Strong", "Talented", "Upbeat", "Valiant", "Wise"
]

animals = [
    "Lion", "Tiger", "Bear", "Eagle", "Shark", "Elephant", "Giraffe", "Dolphin", "Whale",
    "Penguin", "Kangaroo", "Panda", "Wolf", "Fox", "Rabbit", "Deer", "Horse", "Zebra",
    "Leopard", "Cheetah", "Turtle", "Octopus", "Seal", "Otter", "Jellyfish", "Starfish",
    "Crab", "Lobster", "Seahorse", "Clownfish"
]

# Initialiser les credentials Google Sheets à partir de la variable d'environnement
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_info(
    json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON')), scopes=SCOPES
)
spreadsheet_id = "190N64LuG9nEGDa0i7C0kfnXfjqC-FWAtyomqbVjjnTc"  # Utilisation de l'ID fourni
sheet_range = "Noms!A2:A"  # Plage de cellules commençant après l'en-tête

# Route pour l'index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Générer un nom aléatoire
        adjective = random.choice(adjectives)
        animal = random.choice(animals)
        generated_name = f"{adjective} {animal}"

        # Ajouter le nom dans Google Sheets
        success = ajouter_nom_dans_google_sheet(generated_name)

        # Vérifier si l'ajout dans Google Sheets a réussi
        if success:
            return render_template('index.html', nom=generated_name)
        else:
            return render_template('index.html', nom="Erreur d'ajout dans Google Sheets")

    return render_template('index.html')

# Fonction pour ajouter le nom dans Google Sheets
def ajouter_nom_dans_google_sheet(nom):
    try:
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
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout du nom dans Google Sheets: {e}")
        return False

# Lancer l'application
if __name__ == '__main__':
    app.run(debug=True)
