# WARNING: This is a conceptual Python file. You must save and run this
# file separately on your machine (e.g., in your terminal: python server.py).
# This file cannot be edited or run within the current environment.

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random
import re

# 1. Initialize Flask App and Enable CORS
app = Flask(_name_)
# IMPORTANT: This allows your frontend (which is running on a different domain/port) 
# to communicate with this backend.
CORS(app) 

# Simple database/list of known bad keywords for demonstration
PHISHING_KEYWORDS = [
    'login-verify', 
    'update-security', 
    'secure-account', 
    'password-reset', 
    'paypal-billing',
    'bank-transfer'
]

# 2. Define the /predict Endpoint
@app.route('/predict', methods=['GET'])
def predict():
    # Get the URL from the frontend query parameter
    url = request.args.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL parameter missing'}), 400

    # Clean the URL for processing (convert to lowercase)
    url_lower = url.lower()
    
    # 3. Simulate Phishing Detection Logic
    
    # Simple check for demo: Look for bad keywords in the URL string
    is_phishing = False
    for keyword in PHISHING_KEYWORDS:
        if keyword in url_lower:
            is_phishing = True
            break
            
    # Also check if the URL looks like an IP address or contains highly suspicious characters
    if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url_lower):
        is_phishing = True # Flag raw IPs as suspicious

    # Simulate network/processing delay (optional, but good for testing frontend loading states)
    time.sleep(1.5) 

    # 4. Construct the Required JSON Response
    if is_phishing:
        prediction = 'phishing'
        # High confidence for a matched keyword or suspicious pattern
        confidence = random.uniform(0.88, 0.99)
    else:
        prediction = 'safe'
        # High confidence for a seemingly clean URL
        confidence = random.uniform(0.90, 0.98)

    # Return the structured JSON response the frontend expects
    return jsonify({
        'url': url,
        'prediction': prediction,
        'confidence': round(confidence, 4) # Round to 4 decimal places
    })

# 5. Run the Server
if _name_ == '_main_':
    print("----------------------------------------------------------------------")
    print("--- Phishing Defender Backend Running at http://127.0.0.1:8000/ ---")
    print("--- Press Ctrl+C to stop the server. ---------------------------------")
    print("----------------------------------------------------------------------")
    # Running on 127.0.0.1:8000 as required by the frontend script
    app.run(host='127.0.0.1', port=8000, debug=True)