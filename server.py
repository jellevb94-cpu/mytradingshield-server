from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json()
    user_id = (data.get("user_id") or "").strip().lower()

    # laad licenties
    with open("licenses.json", "r", encoding="utf-8") as f:
        licenses = json.load(f)

    record = next((u for u in licenses if u["user_id"].strip().lower() == user_id), None)
    if not record:
        return jsonify({"valid": False, "reason": "not_found"})

    expiry = datetime.strptime(record["valid_until"], "%Y-%m-%d")
    if datetime.now() > expiry:
        return jsonify({"valid": False, "reason": "expired"})

    return jsonify({"valid": True})

@app.route("/", methods=["GET"])
def home():
    return "License server is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
