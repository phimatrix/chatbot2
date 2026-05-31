from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2:1b"

SYSTEM_PROMPT = """You are a helpful assistant for Vanguard Plumbing & Air,
a trusted plumber in Lakeland, FL. Here is everything you know:

SERVICES: Repiping, Drain Cleaning, Clogged Drain Repair, Leak Detection,
Plumbing Inspections, Gas Line Installation, Water Line Repair,
Water Heater Installation. Also provides Air conditioning services.

SERVICE AREAS: Lakeland, Lithia, Bartow, Riverview, Plant City,
Brandon, Lake Wales, Winter Haven, Tampa.

PHONE: 863-213-6583
WEBSITE: vanguardpl.com

POLICIES: Licensed technicians. Upfront pricing. Same-day service
or diagnostic is free. Emergency services available.

Your job:
- Answer questions about services, pricing, and areas we cover
- Collect customer name and phone number if they want a callback
- For emergencies, always give the phone number immediately
- Be friendly, helpful, and professional
- Keep replies short (2-3 sentences max)"""

@app.route("/")
def home():
    return "Vanguard Bot is running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    ollama_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "messages": ollama_messages,
            "stream": False
        })
        result = response.json()
        reply = result["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Sorry, having trouble right now. Please call 863-213-6583!"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
