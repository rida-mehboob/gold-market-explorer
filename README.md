# Gold Market Explorer — 36104 Data Visualisation and Narratives

This is an adapted Streamlit dashboard for the Session 3 Part A final exercise.

## Features
- Summary metrics and a prominent gold-price time series
- Investment fund holdings over time
- Horizontal country ranking of net purchases/sales
- Reported purchases compared with an estimate
- Stacked-area-style export destination comparison
- Country dropdown to explore monthly net buying/selling
- Clear labels identifying all data as synthetic practice data

## Run locally
From this folder, run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy to Streamlit Community Cloud
1. Create a **public GitHub repository**.
2. Upload `app.py`, `requirements.txt`, `README.md`, and the complete `data/` folder to the repository root.
3. Go to https://share.streamlit.io/ and sign in with GitHub.
4. Choose **Create app**, select your repository and branch, and set the main file path to `app.py`.
5. Deploy, then open the app URL in a private/incognito browser window to verify it works.
6. Copy the public `https://....streamlit.app` URL into `submission.txt` and submit that plain-text file through Canvas.

## Important
The data are synthetic and for practice only. If your course expects you to start from its supplied dashboard ZIP or use a specific dataset, adapt this project accordingly and follow your instructor's requirements. I cannot deploy to your GitHub/Streamlit accounts from this package, so the final public URL must be created by you after deployment.
