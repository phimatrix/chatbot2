import requests

history = []
url = "http://127.0.0.1:5000/chat"

def get_reply(user_input):
    history.append({"role": "user", "content": user_input})
    try:
        response = requests.post(url, json={"messages": history}, timeout=30)
        reply = response.json()["reply"]
        history.append({"role": "assistant", "content": reply})
        return reply
    except requests.exceptions.ConnectionError:
        return "ERROR: Cannot connect. Start chatbot_server.py in Terminal 1 first."
    except:
        return "Having trouble. Please call 863-213-6583."

def show_leads():
    try:
        r = requests.get("http://127.0.0.1:5000/leads")
        leads = r.json()
        if not leads:
            print("\n  No customers registered yet.\n")
        else:
            print(f"\n  REGISTERED CUSTOMERS — {len(leads)} total")
            print("  " + "─"*55)
            for i, l in enumerate(leads, 1):
                print(f"  {i}. Name    : {l['Name']}")
                print(f"     Phone   : {l['Phone']}")
                print(f"     Address : {l['Address']}")
                print(f"     Service : {l['Service']}")
                print(f"     Time    : {l['Timestamp']}\n")
    except:
        print("  Could not fetch leads.\n")

print("""
╔══════════════════════════════════════════╗
║  Vanguard Plumbing & Air — AI Assistant  ║
║  Type 'leads' to see registered customers║
║  Type 'clear' to restart conversation    ║
║  Type 'quit' to exit                     ║
╚══════════════════════════════════════════╝
""")

opening = "Thank you for calling Vanguard Plumbing and Air! This is Sarah. How can I assist you today?"
print(f"  Sarah: {opening}\n")

while True:
    try:
        user_input = input("  You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("\n  Sarah: Thank you for contacting Vanguard Plumbing and Air. Have a great day!\n")
            break
        elif user_input.lower() == "leads":
            show_leads()
        elif user_input.lower() == "clear":
            history.clear()
            print("\n  Sarah: Thank you for calling Vanguard Plumbing and Air! This is Sarah. How can I assist you today?\n")
        else:
            print("  Sarah: thinking...", end="\r")
            reply = get_reply(user_input)
            print(f"  Sarah: {reply}\n")
    except KeyboardInterrupt:
        print("\n\n  Goodbye!\n")
        break
