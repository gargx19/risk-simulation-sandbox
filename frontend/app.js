let riskChart = null;

async function runSimulation() {
    const btn = document.getElementById('sim-btn');
    if (btn) {
        btn.disabled = true;
        btn.innerText = "Analyzing Risk...";
        btn.style.cursor = "wait";
    }

    const investment = document.getElementById('investment').value;
    const years = document.getElementById('years').value;
    const stocks = document.getElementById('stocks').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/api/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                initial_investment: parseFloat(investment),
                years: parseInt(years),
                stock_allocation: parseFloat(stocks)
            })
        });

        const json = await response.json();

        if (json.status === "success") {
            const data = json.data;

            // Update Probability Color Mapping
            const probElement = document.getElementById('probability-meter');
            probElement.innerText = `${data.loss_probability}%`;
            if(data.loss_probability < 10) probElement.style.color = '#22c55e'; // Green
            else if (data.loss_probability < 30) probElement.style.color = '#f59e0b'; // Yellow
            else probElement.style.color = '#ef4444'; // Red

            // Update Expected Value & Worst Case
            document.getElementById('expected-meter').innerText = 
                '$' + Math.round(data.expected_value).toLocaleString();
            document.getElementById('worst-meter').innerText = 
                '$' + Math.round(data.worst_case).toLocaleString();

            // Update AI Explainer
            document.getElementById('ai-explainer').innerText = data.ai_explanation;

            // Draw the smooth area chart
            drawChart(data.sample_paths, parseInt(years));
        }
    } catch (error) {
        console.error("Error communicating with backend:", error);
        alert("Failed to connect to the backend. Is your Flask server running?");
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerText = "Simulate Risk";
            btn.style.cursor = "pointer";
        }
    }
}