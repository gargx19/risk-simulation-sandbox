from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import numpy as np

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

def run_monte_carlo(initial_investment, years, expected_return, volatility, num_simulations=1000):
    months = years * 12
    monthly_return = expected_return / 12
    monthly_volatility = volatility / np.sqrt(12)
    
    random_returns = np.random.normal(monthly_return, monthly_volatility, (num_simulations, months))
    cumulative_growth = np.cumprod(1 + random_returns, axis=1)
    
    starting_values = np.full((num_simulations, 1), initial_investment)
    portfolio_paths = np.hstack((starting_values, initial_investment * cumulative_growth))
    
    final_values = portfolio_paths[:, -1]
    
    # Advanced Hackathon Metrics
    loss_probability = (np.sum(final_values < initial_investment) / num_simulations) * 100
    expected_value = np.median(final_values)
    worst_case = np.percentile(final_values, 5)
    
    sample_paths = portfolio_paths[:5].tolist()
    
    return {
        "loss_probability": round(loss_probability, 1),
        "expected_value": round(expected_value, 2),
        "worst_case": round(worst_case, 2),
        "sample_paths": sample_paths
    }

# --- 4. THE ENDPOINT ---
@app.route('/api/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        inv = float(data.get('initial_investment', 10000))
        yrs = int(data.get('years', 10))
        stocks = float(data.get('stock_allocation', 60))

        # Risk profile based on stocks
        stock_ratio = stocks / 100.0
        expected_return = (0.04 * (1 - stock_ratio)) + (0.10 * stock_ratio)
        volatility = (0.03 * (1 - stock_ratio)) + (0.15 * stock_ratio)

        results = run_monte_carlo(inv, yrs, expected_return, volatility)
        
        # Feed math into the AI
        results["ai_explanation"] = get_ai_explanation(
            results["loss_probability"], 
            stocks, 
            yrs, 
            results["expected_value"], 
            results["worst_case"]
        )

        return jsonify({"status": "success", "data": results})
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)