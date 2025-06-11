from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key from the Render environment variable
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    ingredients = data.get('ingredients', [])

    if not ingredients:
        return jsonify({"error": "No ingredients provided."}), 400

    # Build a prompt for the AI
    prompt = (
        f"You are a professional chef. Based on these ingredients: {', '.join(ingredients)}, "
        f"create a creative and delicious recipe. Include the dish name, a list of ingredients, "
        f"and step-by-step instructions."
    )

    try:
        # Send the prompt to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.8
        )

        # Get the AI's reply
        reply = response.choices[0].message.content.strip()

        return jsonify({"recipe": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Make sure it uses the correct port for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
