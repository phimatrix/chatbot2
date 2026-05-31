from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key="YOUR_GEMINI_KEY_HERE")

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction="""You are a helpful assistant for Vanguard Plumbing & Air,
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
)

@app.route("/")
def home():
    return "Vanguard Bot is running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    try:
        history = []
        for msg in messages[:-1]:
            history.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [msg["content"]]
            })
        last_message = messages[-1]["content"]
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(last_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Sorry, I'm having trouble right now. Please call 863-213-6583!"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
