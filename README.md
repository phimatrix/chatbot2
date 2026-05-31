1). first run server in terminal 1
python chatbot_server.py

2). then in terminal 2 run
python chat.py

3). and download all packages like before running above 2 command
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.2:1b
ollama run llama3.2:1b "hello, who are you?"
pip install flask flask-cors requests
then make port public or select public in side of codebar space

4). pip install pyttsx3 SpeechRecognition pyaudio
on local machine for voice 
# Whisper — speech to text
pip install openai-whisper

5). # Piper — needs binary download
wget https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz

6). # Download a natural voice
cd piper
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json

pip install openai-whisper sounddevice soundfile numpy
