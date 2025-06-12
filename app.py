from flask import Flask, request, jsonify
from transformers import pipeline
import os

app = Flask(__name__)

# Load HF model (small, CPU-friendly model)
# You can experiment with other text-generation models here if you want
generator = pipeline("text-generation", model="tiiuae/falcon-rw-1b", token=os.environ.get("HF_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    ingredients = data.get("ingredients", [])
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    prompt = (
        f"You're a master chef. Using these ingredients: {', '.join(ingredients)}, "
        "write a complete recipe including the dish name, prep/cook time, oven temperature (if needed), tools, "
        "and step-by-step instructions. Keep it realistic and clear."
    )

    try:
        result = generator(prompt, max_new_tokens=300, do_sample=True, temperature=0.7)
        recipe = result[0]["generated_text"]
        return jsonify({"recipe": recipe})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
