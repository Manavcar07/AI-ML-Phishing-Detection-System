PhishingDetector - demo starter project

Files in this archive:
- dataset_small.csv : small synthetic dataset (for demo)
- phishing_model.pkl : trained RandomForest model (small demo)
- predict_model.py : CLI helper to test model locally
- backend/app.py : FastAPI backend (loads phishing_model.pkl)
- extension/* : Chrome extension files (manifest.json, popup.html, popup.js, icon.png)
- README.txt : this file

How to run:
1) Install Python packages:
   pip install scikit-learn pandas fastapi uvicorn

2) Start backend:
   cd PhishingDetector/backend
   python app.py
   (Or: uvicorn app:app --reload --host 127.0.0.1 --port 8000)

3) Load Chrome extension:
   - Open Chrome -> Extensions -> Load unpacked -> select PhishingDetector/extension folder
   - Click the extension icon -> Click "Check Current Site"

4) Test model from command line:
   cd PhishingDetector
   python predict_model.py "http://secure-login-google.com/verify"

Notes:
- This is a simple demo model trained on a tiny synthetic dataset. For real-world use, you must train on large, curated datasets and add more robust features.
- Backend and extension communicate over localhost; ensure backend is running before using extension.
