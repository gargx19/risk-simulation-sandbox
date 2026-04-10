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

def get_ai_explanation(loss_prob, stock_allocation, years, expected_val, worst_case):
    prompt = f"""
    You are an expert financial advisor for a Fintech app. A user is testing a portfolio with {stock_allocation}% stocks over {years} years.
    - Loss Probability: {loss_prob}%
    - Expected Median Value: ${expected_val:,.0f}
    - Worst Case Scenario: ${worst_case:,.0f}
    
    Write a short, engaging 3-sentence analysis. Use bullet points for readability. Be encouraging but realistic. Do not use markdown bolding (**) in your response.
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant", # The fast, current Groq model
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n--- AI ERROR --- \n{e}\n----------------\n")
        return "• Simulation successful.\n• Your math is sound.\n• Stay invested for the long term to mitigate volatility."

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online", 
        "message": "Risk Simulator API is running. Ready for Monte Carlo math!"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)