from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL = "llama3.2:1b"
LEADS_FILE = "leads.csv"

if not os.path.exists(LEADS_FILE):
    with open(LEADS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Address", "Service", "Timestamp"])

SYSTEM_PROMPT = """You are Sarah, a professional customer service representative for Vanguard Plumbing & Air, based in Lakeland, Florida, USA.

COMPANY INFO:
- Services: Repiping, Drain Cleaning, Clogged Drain Repair, Leak Detection, Plumbing Inspections, Gas Line Installation, Water Line Repair, Water Heater Installation, Air Conditioning
- Service Areas (USA only): Lakeland, Lithia, Bartow, Riverview, Plant City, Brandon, Lake Wales, Winter Haven, Tampa — all in Florida, USA
- Phone: 863-213-6583
- Website: vanguardpl.com
- Hours: 24/7 for emergencies

PERSONALITY:
- Warm, professional, concise
- Never reveal you are an AI or mention steps/rules
- Sound like a real receptionist named Sarah
- Maximum 2 sentences per reply unless collecting info

SERVICE AREA RULE:
- If customer mentions any location outside Florida, USA — politely say we only serve Florida and ask if they are located in our service area
- Do not proceed with booking if customer is outside Florida

BOOKING FLOW — collect one at a time, naturally:
1. If customer wants service → ask their full name warmly
2. Got name → ask for their phone number
3. Got phone → ask for their full address in Florida
4. If address is outside Florida/USA → say we only serve Florida, do not save
5. Got valid Florida address → ask what service they need (if not already mentioned)
6. Got all 4 → output this tag on its own line:
SAVE_LEAD:name=VALUE|phone=VALUE|address=VALUE|service=VALUE
Then say: "Perfect! I have got everything noted down. One of our technicians will call you at [phone] within the hour to confirm your appointment. Is there anything else I can help you with?"

EMERGENCY: Always give 863-213-6583 immediately for urgent issues like burst pipes or gas leaks."""

def save_lead(name, phone, address, service):
    with open(LEADS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, address, service, datetime.now().strftime("%Y-%m-%d %H:%M")])
    print(f"\n{'='*55}")
    print(f"  NEW CUSTOMER REGISTERED!")
    print(f"  Name    : {name}")
    print(f"  Phone   : {phone}")
    print(f"  Address : {address}")
    print(f"  Service : {service}")
    print(f"  Time    : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*55}\n")

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
        reply = response.json()["message"]["content"]
        if "SAVE_LEAD:" in reply:
            try:
                lead_line = [l for l in reply.split("\n") if "SAVE_LEAD:" in l][0]
                lead_data = lead_line.split("SAVE_LEAD:")[1].strip()
                parts = {}
                for item in lead_data.split("|"):
                    if "=" in item:
                        key, val = item.split("=", 1)
                        parts[key.strip()] = val.strip()
                name    = parts.get("name", "")
                phone   = parts.get("phone", "")
                address = parts.get("address", "")
                service = parts.get("service", "")
                if name and phone and address and service:
                    save_lead(name, phone, address, service)
                reply = reply.replace(lead_line, "").strip()
            except Exception as e:
                print(f"Lead parse error: {e}")
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "I apologize for the inconvenience. Please call us directly at 863-213-6583 and our team will assist you right away."}), 200

@app.route("/leads", methods=["GET"])
def view_leads():
    leads = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                leads.append(row)
    return jsonify(leads)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
