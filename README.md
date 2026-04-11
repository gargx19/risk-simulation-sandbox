# 📈 Risk Simulation Sandbox  
### Demystifying Investment Fear  
Finvasia Innovation Hackathon 2026 Submission  
Organized by Chitkara University in collaboration with Finvasia  

---

## The Problem
Retail investors often avoid the stock market due to a lack of understanding of risk and volatility.

Most traditional financial tools:
- Use complex financial jargon  
- Rely on static or linear calculators  
- Fail to represent real-world uncertainty  

This leads to "investment fear", preventing individuals from participating in long-term financial growth.

---

## Our Solution
Risk Simulation Sandbox is an AI-powered platform that transforms complex financial concepts into simple, understandable insights.

Key capabilities:
- Runs 1000+ Monte Carlo simulations to model market behavior  
- Calculates:
  - Loss Probability  
  - Median Expected Value  
  - Worst-case scenarios (bottom 5%)  
- Uses a Large Language Model (Llama 3.1 via Groq) to generate clear, human-readable financial explanations  

The platform helps users understand risk instead of avoiding it.

---

## Technology Stack

### Backend (Core Intelligence)
- Python and NumPy for numerical computation and simulation  
- Groq API (Llama-3.1-8b-instant) for real-time AI inference  

### Frontend (Interface Layer)
- HTML5 and CSS3 for responsive UI  
- Chart.js for data visualization  

### Integration
- Flask and Flask-CORS for API development and communication  

---

## How to Run the Project

### Prerequisites
- Python 3.8 or above  
- Groq API Key  

---

### Step 1: Clone Repository
```bash
git clone https://github.com/gargx19/risk-simulation-sandbox.git
cd risk-simulation-sandbox
    # Step 2: Setup Backend
cd backend
python -m venv venv
    # Activate Virtual Environment
    ## Windows
venv\Scripts\activate
    ## Mac/Linux
source venv/bin/activate
    # Step 4: Install Dependencies
pip install flask flask-cors numpy groq
    # Step 5: Add API Key
    ## Open backend/app.py and replace:
GROQ_API_KEY = "PASTE_YOUR_GROQ_KEY_HERE"
    # Step 6: Run Backend
python app.py
    # Step 7: Run Frontend
    ## Open the following file in your browser:
frontend/index.html
```

👥 Team Composition
- Krish Garg
    * Lead Backend Developer & System Architect
    * Architected the Flask API and server-side infrastructure.
    * Implemented the Monte Carlo simulation engine using NumPy.
    * Managed the end-to-end integration and repository structure.

- Lipika
    * AI Engineer & Integration Specialist
    * Developed the "Core Intelligence" logic using Llama-3.1 via Groq.
    * Crafted the AI prompting strategy for personalized financial coaching.
    * Managed the primary frontend-to-backend communication layer.

- Diksha
    * UI/UX Designer & Frontend Architect
    * Designed and built the responsive, dark-themed dashboard interface.
    * Developed the custom CSS design system and interactive slider controls.
    * Ensured the "Interface Layer" met high-quality usability standards.

-Devanshu
    * Data Visualization Engineer
    * Engineered the dynamic Chart.js logic for real-time risk visualization.
    * Implemented the gradient-mapped path rendering for simulation results.
    * Optimized the presentation of complex analytical data for retail users.