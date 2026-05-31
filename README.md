first run server in terminal 1
python chatbot_server.py

then in terminal 2 run
python chat.py

and download all packages like before running above 2 command
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
ollama pull llama3.2:1b
ollama run llama3.2:1b "hello, who are you?"
pip install flask flask-cors requests
then make port public or select public in side of codebar space

