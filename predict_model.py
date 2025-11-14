
import pickle, sys
import re
def extract_features(url):
    f_url = url.lower()
    url_length = len(url)
    num_digits = sum(c.isdigit() for c in url)
    num_special = sum(not c.isalnum() for c in url)
    has_https = 1 if f_url.startswith("https") else 0
    num_subdomains = f_url.count(".")
    has_ip = 1 if __import__('re').search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", url) else 0
    suspicious_words = int(any(k in f_url for k in ["login","secure","verify","confirm","update","claim","account","auth","bank","pay","secure-login","verify-account","confirm"]))
    return [url_length, num_digits, num_special, has_https, num_subdomains, has_ip, suspicious_words]

model = pickle.load(open("phishing_model.pkl","rb"))
if len(sys.argv) < 2:
    print("Usage: python predict_model.py <url>")
else:
    url = sys.argv[1]
    feats = [extract_features(url)]
    pred = model.predict(feats)[0]
    prob = model.predict_proba(feats)[0].max()
    print({"url": url, "prediction": "phishing" if pred==1 else "safe", "confidence": float(prob)})
