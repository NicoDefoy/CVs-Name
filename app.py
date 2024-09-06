from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
# Configuration de la base de données PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://name_28lm_user:gibotS0rQWxfueyp7chiM8P5bgztd4lp@dpg-crc70i3v2p9s73dn1p20-a.frankfurt-postgres.render.com/name_28lm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class NomGenere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<NomGenere {self.nom}>'

with app.app_context():
    try:
        print("Tentative de création des tables dans la base de données...")
        db.create_all()
        print("Les tables ont été créées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")

@app.route('/')
def index():
    print("Page d'accueil demandée...")
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    print("Requête POST reçue", flush=True)
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

    while True:
        adj = random.choice(adjectives)
        animal = random.choice(animals)
        nom = f"{adj} {animal}"
        print(f"Nom généré : {nom}", flush=True)

        if not NomGenere.query.filter_by(nom=nom).first():
            print(f"Ajout du nom : {nom} à la base de données", flush=True)
            nouveau_nom = NomGenere(nom=nom)
            db.session.add(nouveau_nom)
            db.session.commit()
            break
        else:
            print(f"Nom {nom} déjà existant, génération d'un nouveau nom", flush=True)

    return render_template('index.html', nom=nom)

if __name__ == '__main__':
    print("Démarrage de l'application Flask...")
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)

