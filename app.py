from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

# Utiliser l'URL PostgreSQL de Railway
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qTqKLbmwfwWmLEkUlGupYSAsduWIRqDOZ@meticulous-empathy-postgresql.railway.app:5432/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèle de données pour les noms générés
class NomGenere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<NomGenere {self.nom}>'

# Créer la base de données et les tables si elles n'existent pas déjà
with app.app_context():
    db.create_all()

# Listes d'adjectifs positifs et de noms d'animaux connus
adjectifs = [
    "Amazing", "Brilliant", "Clever", "Dazzling", "Excellent", "Fantastic", "Glorious", "Heroic", "Incredible", "Joyful",
    "Kind", "Luminous", "Magnificent", "Noble", "Outstanding", "Powerful", "Quick", "Radiant", "Spectacular", "Wonderful",
    "Unique", "Vibrant", "Wonderful", "Xenial", "Youthful", "Zealous", "Adventurous", "Bold", "Creative", "Determined",
    "Energetic", "Fearless", "Generous", "Humble", "Innovative", "Jovial", "Keen", "Lively", "Motivated", "Nurturing",
    "Optimistic", "Passionate", "Quirky", "Resilient", "Strong", "Talented", "Upbeat", "Valiant", "Wise"
]

animaux = [
    "Lion", "Tiger", "Bear", "Eagle", "Shark", "Elephant", "Giraffe", "Dolphin", "Whale", "Penguin",
    "Kangaroo", "Panda", "Wolf", "Fox", "Rabbit", "Deer", "Horse", "Zebra", "Leopard", "Cheetah",
    "Turtle", "Octopus", "Seal", "Otter", "Jellyfish", "Starfish", "Crab", "Lobster", "Seahorse", "Clownfish"
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    print("Requête POST reçue", flush=True)
    while True:
        adj = random.choice(adjectifs)
        animal = random.choice(animaux)
        nom = f"{adj} {animal}"
        print(f"Nom généré : {nom}", flush=True)
        
        # Vérifie si le nom existe déjà dans la base de données
        try:
            if not NomGenere.query.filter_by(nom=nom).first():
                print(f"Ajout du nom : {nom} à la base de données", flush=True)
                nouveau_nom = NomGenere(nom=nom)
                db.session.add(nouveau_nom)
                db.session.commit()
                break
            else:
                print(f"Nom {nom} déjà existant, génération d'un nouveau nom", flush=True)
        except Exception as e:
            print(f"Erreur lors de l'ajout à la base de données : {e}", flush=True)
            db.session.rollback()

    return render_template('index.html', nom=nom)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))  # Change le port par défaut à 8000
    app.run(debug=True, host='0.0.0.0', port=port)

