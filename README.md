# ⚙️ Gear Train Ratio & Speed Calculator — Mr. Pythons

**Topic 23 — Simple & Compound Gear Train Ratio & Speed Calculator**
Diploma in Mechanical Engineering, Semester 3 — Python Mini Project (Streamlit)

**Group:** Mr. Pythons
**Members:**
- Abdul Mukhtadir Faizaan — 25012250610060
- Akshit Valand — 25012251210007
- Daksh Talsaniya — 25012251210006
- Shaikh Mohammed Jalis — 24012250670909

**Guide:** Shaikh Mohammed Azim

## Features
- Simple **and** Compound gear train modes
- Speed ratio (train value), output speed, rotation direction, output torque,
  mechanical advantage, and power balance
- All formulas shown in the app (LaTeX)
- Input validation (minimum teeth count, positive speed/efficiency)
- 3D animated gear model (Plotly) rotating at the true calculated speed & direction
- Matplotlib graphs: speed distribution, sensitivity analysis, torque/power comparison
- White / Blue / Black theme

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push `app.py` and `requirements.txt` to a public GitHub repository.
2. Go to [streamlit.io](https://streamlit.io) → sign in with GitHub.
3. Click **New app**, select this repo and `app.py`, then **Deploy**.
4. Copy the live app link for submission.
