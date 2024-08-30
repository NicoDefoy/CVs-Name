from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Listes d'adjectifs positifs et de noms d'animaux connus
adjectifs = [
    "Amazing", "Brilliant", "Clever", "Dazzling", "Excellent", "Fantastic", "Glorious", "Heroic", "Incredible", "Joyful",
    "Kind", "Luminous", "Magnificent", "Noble", "Outstanding", "Powerful", "Quick", "Radiant", "Spectacular", "Terrific",
    "Unique", "Vibrant", "Wonderful", "Xenial", "Youthful", "Zealous", "Adventurous", "Bold", "Creative", "Determined",
    "Energetic", "Fearless", "Generous", "Humble", "Innovative", "Jovial", "Keen", "Lively", "Motivated", "Nurturing",
    "Optimistic", "Passionate", "Quirky", "Resilient", "Strong", "Talented", "Upbeat", "Valiant", "Wise"
]

animaux = [
    "Lion", "Tiger", "Bear", "Eagle", "Shark", "Elephant", "Giraffe", "Dolphin", "Whale", "Penguin",
    "Kangaroo", "Panda", "Wolf", "Fox", "Rabbit", "Deer", "Horse", "Zebra", "Leopard", "Cheetah",
    "Turtle", "Octopus", "Seal", "Otter", "Jellyfish", "Starfish", "Crab", "Lobster", "Seahorse", "Clownfish"
]

# Set pour stocker les noms générés
noms_generes = set()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    while True:
        adj = random.choice(adjectifs)
        animal = random.choice(animaux)
        nom = f"{adj} {animal}"
        if nom not in noms_generes:
            noms_generes.add(nom)
            break
    return render_template('index.html', nom=nom)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)