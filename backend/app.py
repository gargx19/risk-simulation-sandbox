from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq 

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = "PASTE_YOUR_GROQ_KEY_HERE"
try:
    client = Groq(api_key=GROQ_API_KEY)
    print("Groq System Initialized Successfully!")
except Exception as e:
    print(f"Setup Error: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online", 
        "message": "Risk Simulator API is running. Ready for Monte Carlo math!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)