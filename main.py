import os
import threading
import webbrowser
import subprocess
from flask import Flask, jsonify
from flask_cors import CORS
from predictor import RacePredictor
from ai_analyst import AIAnalyst

app = Flask(__name__)
CORS(app)

predictor = RacePredictor()
analyst = AIAnalyst()

@app.route('/predict', methods=['GET'])
def predict():
    sample_runners = [
        {"name": "Runner 1", "rating": 88, "form": 90},
        {"name": "Runner 2", "rating": 75, "form": 82},
        {"name": "Runner 3", "rating": 92, "form": 88}
    ]
    predictions = predictor.calculate_probabilities(sample_runners)
    analysis = analyst.analyze_race([
        {"name": r["runner"], "score": float(r["win_prob"].replace('%', '')) * 2} 
        for r in predictions
    ])
    
    return jsonify({
        "status": "Active",
        "predictions": predictions,
        "analysis": analysis
    })

def open_browser(url):
    """Automatically opens the app UI upon server startup."""
    try:
        # Try Android/Termux native opener first
        subprocess.run(["termux-open-url", url], check=True)
    except Exception:
        # Fallback to standard Python webbrowser launcher
        webbrowser.open(url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    target_url = f"http://127.0.0.1:{port}/predict"
    
    # Launch browser thread 1.5 seconds after execution so server is ready
    threading.Timer(1.5, open_browser, args=[target_url]).start()
    
    app.run(host='0.0.0.0', port=port)
