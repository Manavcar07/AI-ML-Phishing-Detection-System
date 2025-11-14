document.getElementById('check').addEventListener('click', () => {
  // Fetch the active tab URL
  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    const url = tabs[0].url;

    const resultBox = document.getElementById('result');
    resultBox.innerText = 'Checking...';
    resultBox.style.color = 'black';

    // Call backend API
    fetch('http://127.0.0.1:8000/predict?url=' + encodeURIComponent(url))
      .then((r) => r.json())
      .then((data) => {
        // Show result text
        resultBox.innerText = `Site: ${data.url}
Result: ${data.prediction}
Confidence: ${Math.round(data.confidence * 100)}%`;

        // Apply colors
        if (data.prediction === 'phishing') {
          resultBox.style.color = 'red';
        } else {
          resultBox.style.color = 'green';
        }
      })
      .catch(() => {
        resultBox.innerText = 'Error: Could not connect to backend.';
        resultBox.style.color = 'orange';
      });
  });
});
