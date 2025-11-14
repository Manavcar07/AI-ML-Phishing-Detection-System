import pandas as pd
import numpy as np
import pickle
import re
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import tldextract

# Optional advanced modules
try:
    import whois
except:
    whois = None

try:
    import requests
except:
    requests = None

def get_domain(url):
    ext = tldextract.extract(url)
    domain = ext.domain + "." + ext.suffix
    return domain.lower()

def get_tld_score(url):
    ext = tldextract.extract(url)
    tld = ext.suffix

    risky_tlds = ["xyz", "top", "work", "click", "gq", "ml", "cf", "tk", "ga", "online"]
    if tld in risky_tlds:
        return 1
    return 0

def levenshtein(a, b):
    """Distance calculation for brand copy detection."""
    dp = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)+1):
        dp[i][0] = i
    for j in range(len(b)+1):
        dp[0][j] = j
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            cost = 0 if a[i-1]==b[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
            )
    return dp[-1][-1]

def brand_similarity(url):
    brand_list = ["google","facebook","amazon","paypal","instagram","microsoft","apple"]
    domain = get_domain(url)

    min_distance = min([levenshtein(domain.split(".")[0], brand) for brand in brand_list])

    return min_distance

def domain_age_days(url):
    if not whois:
        return -1
    try:
        d = get_domain(url)
        w = whois.whois(d)
        cd = w.creation_date
        if isinstance(cd, list):
            cd = cd[0]
        if isinstance(cd, str):
            cd = datetime.fromisoformat(cd)
        if cd:
            return (datetime.now() - cd).days
    except:
        return -1
    return -1

def redirect_count(url):
    if not requests:
        return 0
    try:
        r = requests.get(url, timeout=4, allow_redirects=True)
        return len(r.history)
    except:
        return 0

def extract_features(url):

    f_url = url.lower()
    domain = get_domain(url)

    features = [
        len(url),
        sum(c.isdigit() for c in url),
        sum(not c.isalnum() for c in url),
        f_url.count("."),
        1 if f_url.startswith("https") else 0,
        1 if re.search(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", url) else 0,
        int(any(k in f_url for k in ["login","secure","verify","update","account","auth"])),
        f_url.count("-"),
        get_tld_score(url),
        brand_similarity(url),
        domain_age_days(url),
        redirect_count(url)
    ]

    return features

df = pd.read_csv("dataset_small.csv")

X = np.array([extract_features(u) for u in df["url"]])
y = df["label"].values

model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X, y)

pickle.dump(model, open("phishing_model.pkl", "wb"))

print("Advanced model trained and saved as phishing_model.pkl")

