from flask import Flask, request, jsonify
import os
import traceback
from openai import OpenAI

app = Flask(__name__)

client = OpenAI()

@app.route('/')
def home():
    return "Webhook is live!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json(force=True)
        ingredients = data.get('ingredients', [])

        if not ingredients:
            return jsonify({"error": "No ingredients provided"}), 400

        prompt = f"Create a delicious recipe using these ingredients: {', '.join(ingredients)}. Include a name, ingredients list, cooking steps, time, and a final tip."

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful chef."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        recipe = response.choices[0].message.content
        return jsonify({"recipe": recipe})

    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": "Something went wrong on the server."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
