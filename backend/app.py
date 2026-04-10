from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online", 
        "message": "Risk Simulator API is running. Ready for Monte Carlo math!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)