from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()

app = Flask(__name__)
CORS(app)

# --- 1. CONFIGURATION ---
# Load API key from environment variable (set in .env or system env)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY environment variable not set.")

try:
    client = Groq(api_key=GROQ_API_KEY)
    print("Groq System Initialized Successfully!")
except Exception as e:
    print(f"Setup Error: {e}")

# --- 2. AI ENGINE ---
def get_ai_explanation(loss_prob, stock_allocation, years, expected_val, worst_case, initial_investment):
    prompt = f"""
    You are a friendly and encouraging financial coach inside an investment simulation app called 'InvestSafe Sandbox'.
    A young user has just tested a portfolio scenario with the following results:
    - Initial Investment: ${initial_investment:,.0f}
    - Stock Allocation: {stock_allocation}%
    - Time Horizon: {years} years
    - Loss Probability: {loss_prob}%
    - Expected Median Portfolio Value: ${expected_val:,.0f}
    - Worst Case (5th percentile) Value: ${worst_case:,.0f}

    Write a short, engaging 3-bullet analysis. Each bullet should be one clear sentence.
    Be encouraging but realistic. Help reduce fear of investing by contextualizing the numbers.
    Do not use markdown bolding (**) in your response. Use plain bullet points (•).
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"\n--- AI ERROR --- \n{e}\n----------------\n")
        return (
            "• Even in the worst simulated outcomes, staying invested long-term historically recovers losses.\n"
            "• Your expected portfolio growth shows the power of compounding over time.\n"
            "• Starting early and staying consistent is the most effective strategy for wealth building."
        )

# --- 3. MATH ENGINE (Monte Carlo Simulation) ---
def run_monte_carlo(initial_investment, years, expected_return, volatility, num_simulations=1000):
    months = years * 12
    monthly_return = expected_return / 12
    monthly_volatility = volatility / np.sqrt(12)

    random_returns = np.random.normal(monthly_return, monthly_volatility, (num_simulations, months))
    cumulative_growth = np.cumprod(1 + random_returns, axis=1)

    starting_values = np.full((num_simulations, 1), initial_investment)
    portfolio_paths = np.hstack((starting_values, initial_investment * cumulative_growth))

    final_values = portfolio_paths[:, -1]

    loss_probability = (np.sum(final_values < initial_investment) / num_simulations) * 100
    expected_value = np.median(final_values)
    worst_case = np.percentile(final_values, 5)
    best_case = np.percentile(final_values, 95)

    # Return 5 sample paths for charting
    sample_paths = portfolio_paths[:5].tolist()

    return {
        "loss_probability": round(loss_probability, 1),
        "expected_value": round(expected_value, 2),
        "worst_case": round(worst_case, 2),
        "best_case": round(best_case, 2),
        "sample_paths": sample_paths
    }

# --- 4. SIMULATE ENDPOINT ---
@app.route('/api/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        inv = float(data.get('initial_investment', 10000))
        yrs = int(data.get('years', 10))
        stocks = float(data.get('stock_allocation', 60))

        if not (0 <= stocks <= 100):
            return jsonify({"status": "error", "message": "stock_allocation must be between 0 and 100"}), 400
        if not (1 <= yrs <= 40):
            return jsonify({"status": "error", "message": "years must be between 1 and 40"}), 400
        if inv <= 0:
            return jsonify({"status": "error", "message": "initial_investment must be positive"}), 400

        stock_ratio = stocks / 100.0
        expected_return = (0.04 * (1 - stock_ratio)) + (0.10 * stock_ratio)
        volatility = (0.03 * (1 - stock_ratio)) + (0.15 * stock_ratio)

        results = run_monte_carlo(inv, yrs, expected_return, volatility)

        results["ai_explanation"] = get_ai_explanation(
            results["loss_probability"],
            stocks,
            yrs,
            results["expected_value"],
            results["worst_case"],
            inv
        )

        return jsonify({"status": "success", "data": results})
    except Exception as e:
        print(f"General Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- 5. HEALTH CHECK ---
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "InvestSafe Sandbox API is running."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
