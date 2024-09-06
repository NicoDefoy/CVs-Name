from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://name_28lm_user:gibotS0rQWxfueyp7chiM8P5bgztd4lp@dpg-crc70i3v2p9s73dn1p20-a.frankfurt-postgres.render.com/name_28lm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle pour la base de données
class NomGenere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

# Création de la base de données
with app.app_context():
    db.create_all()

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
        
        # Enregistrer dans la base de données
        nouveau_nom = NomGenere(nom=generated_name)
        db.session.add(nouveau_nom)
        db.session.commit()

        return render_template('index.html', nom=generated_name)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

