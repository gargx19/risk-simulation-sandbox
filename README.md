# 🧠 InvestSafe Sandbox — Investigating Fear
### Finvasia Innovation Hackathon 2026 | Team Tech4

> An AI-powered investment risk simulator that uses Monte Carlo simulations and a Large Language Model to help young investors overcome psychological barriers to investing.

---

## 📌 Problem Statement
**Investigating Fear** — Young users fear investing due to fear of loss. If investing risk is contextualized and loss is simulated before real exposure, fear can reduce.

---

## 💡 Solution
**InvestSafe Sandbox** runs **1,000 parallel Monte Carlo simulations** to model real market uncertainty. An AI coach (Llama 3.1 via Groq) then translates the raw numbers into an empathetic, plain-English narrative — making risk feel approachable rather than frightening.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| AI/ML | Llama-3.1-8b-instant via Groq API |
| Backend | Python 3.10+, Flask, NumPy |
| Frontend | HTML5, CSS3, Vanilla JavaScript, Chart.js |
| API | Flask REST API with CORS support |

---

## 📁 Project Structure

```
project/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment variable template
├── frontend/
│   └── index.html          # Single-page UI
└── README.md
```

---

## ⚡ Setup & Run

### Prerequisites
- Python 3.10 or higher
- A free [Groq API Key](https://console.groq.com/)

### Step 1 — Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2 — Configure API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and paste your Groq API key:
# GROQ_API_KEY=your_actual_key_here
```

### Step 3 — Start the Backend

```bash
python app.py
# Server runs at http://localhost:5000
# Visit http://localhost:5000/api/health to confirm it's running
```

### Step 4 — Open the Frontend

```bash
# Simply open frontend/index.html in any browser
# No build step required
```

---

## 🔌 API Reference

### `POST /api/simulate`

**Request Body:**
```json
{
  "initial_investment": 100000,
  "years": 10,
  "stock_allocation": 60
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "loss_probability": 12.3,
    "expected_value": 178500.00,
    "worst_case": 89200.00,
    "best_case": 320000.00,
    "sample_paths": [[...], ...],
    "ai_explanation": "• Your portfolio has a strong chance..."
  }
}
```

### `GET /api/health`
Returns `{"status": "ok"}` if the server is running.

---

## ✨ Key Features

- **Monte Carlo Engine** — 1,000 market simulations using NumPy's normal distribution
- **AI Financial Coach** — Llama 3.1 generates personalized, empathetic risk analysis in real-time
- **Loss Probability Meter** — Visual bar showing probability of losing money
- **Portfolio Path Chart** — 5 sample simulation trajectories plotted interactively
- **Interactive Sliders** — Real-time updates for stock allocation and time horizon

---

## 👥 Team Tech4

| Name | Role |
|------|------|
| Krish Garg | Team Lead |
| Lipika | Frontend Developer |
| Diksha | AI/ML Integration |
| Devanshu Garg | Backend Developer |

---

## 🔮 Future Scope

- Integration with Finvasia's live trading APIs for real market data
- User accounts to track simulations over time
- SIP (Systematic Investment Plan) simulation mode
- Mobile-responsive PWA version
