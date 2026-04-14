import os
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

COLAB_API_URL = "https://storeroom-donated-handstand.ngrok-free.dev/api/chat"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("message", "")
    if not question:
        return jsonify({"response": "Please ask something."})

    try:
        res = requests.post(
            COLAB_API_URL,
            json={"text": question},
            headers={
                "ngrok-skip-browser-warning": "69420",
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json"
            },
            timeout=120
        )
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text[:300]}")
        res.raise_for_status()
        reply = res.json().get("reply", "No response received.")
        # Strip the echoed prompt if model returns it
        if question in reply:
            reply = reply.replace(question, "").strip()
        return jsonify({"response": reply})
    except requests.exceptions.Timeout:
        return jsonify({"response": "Request timed out. The model may be busy."})
    except Exception as e:
        return jsonify({"response": f"Error contacting model: {str(e)}"})

if __name__ == "__main__":
    print("Monarch AI ready (Colab backend)!")
    app.run(debug=False, port=5000)
