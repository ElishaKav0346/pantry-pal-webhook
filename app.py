from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    
    # For demo, just echo back the ingredients with a sample recipe
    recipe = {
        "name": "Sample Omelette",
        "ingredients": ingredients,
        "instructions": [
            "Crack the eggs into a bowl.",
            "Whisk the eggs with salt and pepper.",
            "Heat a pan and pour the eggs in.",
            "Cook until firm and fold over.",
            "Serve hot."
        ]
    }
    return jsonify(recipe)

if __name__ == '__main__':
    app.run(debug=True)
