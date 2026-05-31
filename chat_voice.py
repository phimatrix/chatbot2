import requests
import subprocess
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os

# Load whisper model once at startup
print("  Loading Whisper model...")
whisper_model = whisper.load_model("base.en")
print("  Whisper ready!")

PIPER_PATH = "./piper/piper"
PIPER_MODEL = "./piper/en_US-lessac-medium.onnx"

history = []
url = "http://127.0.0.1:5000/chat"
voice_mode = False

def speak_piper(text):
    """Convert text to speech using Piper — natural voice"""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            out_file = f.name
        subprocess.run(
            [PIPER_PATH, "--model", PIPER_MODEL, "--output_file", out_file],
            input=text.encode(),
            capture_output=True
        )
        data, samplerate = sf.read(out_file)
        sd.play(data, samplerate)
        sd.wait()
        os.unlink(out_file)
    except Exception as e:
        print(f"  (Piper error: {e})")

def listen_whisper():
    """Record mic and transcribe using Whisper"""
    print("  🎤 Listening... (5 seconds)")
    try:
        duration = 5
        samplerate = 16000
        recording = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype='float32'
        )
        sd.wait()
        audio = np.squeeze(recording)
        result = whisper_model.transcribe(audio, language="en")
        text = result["text"].strip()
        if text:
            print(f"  You said: {text}")
            return text
        return None
    except Exception as e:
        print(f"  (Whisper error: {e})")
        return None

def get_reply(user_input):
    history.append({"role": "user", "content": user_input})
    try:
        response = requests.post(url, json={"messages": history}, timeout=30)
        reply = response.json()["reply"]
        history.append({"role": "assistant", "content": reply})
        return reply
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
║  Vanguard Plumbing & Air — Voice Assistant
║  voice on  → Sarah speaks replies        ║
║  mic       → Speak your message          ║
║  leads     → See registered customers    ║
║  quit      → Exit                        ║
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
            msg = "Thank you for contacting Vanguard Plumbing and Air. Have a great day!"
            print(f"\n  Sarah: {msg}\n")
            if voice_mode:
                speak_piper(msg)
            break

        elif user_input.lower() == "voice on":
            voice_mode = True
            print("  ✅ Voice mode ON — Sarah will speak using Piper.\n")
            continue

        elif user_input.lower() == "voice off":
            voice_mode = False
            print("  🔇 Voice mode OFF.\n")
            continue

        elif user_input.lower() == "mic":
            spoken = listen_whisper()
            if spoken:
                user_input = spoken
            else:
                print("  Could not understand. Please type instead.\n")
                continue

        elif user_input.lower() == "leads":
            show_leads()
            continue

        elif user_input.lower() == "clear":
            history.clear()
            print("\n  Sarah: Thank you for calling Vanguard Plumbing and Air! This is Sarah. How can I assist you today?\n")
            continue

        print("  Sarah: thinking...", end="\r")
        reply = get_reply(user_input)
        print(f"  Sarah: {reply}\n")
        if voice_mode:
            speak_piper(reply)

    except KeyboardInterrupt:
        print("\n\n  Goodbye!\n")
        break
