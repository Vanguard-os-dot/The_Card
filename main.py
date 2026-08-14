import os
import threading
import subprocess
import webbrowser
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from predictor import RacePredictor
from ai_analyst import AIAnalyst

app = Flask(__name__, static_folder='.')
CORS(app)

predictor = RacePredictor()
analyst = AIAnalyst()

# 1. Root route serves your actual frontend app
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# 2. API endpoint handles prediction calculations
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json() or {}
        sample_runners = data.get("runners", [])
    else:
        sample_runners = [
            {"name": "Red Coral", "rating": 72, "form": 82},
            {"name": "Poursomesugaronme", "rating": 74, "form": 78},
            {"name": "Oklahoma Girl", "rating": 68, "form": 70}
        ]
    
    if not sample_runners:
        return jsonify({"error": "No runners provided"}), 400

    predictions = predictor.calculate_probabilities(sample_runners)
    
    formatted_for_analysis = []
    for r in predictions:
        try:
            prob_val = float(r["win_prob"].replace('%', ''))
        except ValueError:
            prob_val = 0.0
        formatted_for_analysis.append({"name": r["runner"], "score": prob_val * 2})

    analysis = analyst.analyze_race(formatted_for_analysis)
    
    return jsonify({
        "status": "Active",
        "predictions": predictions,
        "analysis": analysis
    })

def auto_launch(url):
    try:
        subprocess.run(["termux-open-url", url], check=True)
    except Exception:
        webbrowser.open(url)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    # Open the HTML interface at http://127.0.0.1:5050/
    threading.Timer(1.5, auto_launch, args=[f"http://127.0.0.1:{port}/"]).start()
    app.run(host='0.0.0.0', port=port)
