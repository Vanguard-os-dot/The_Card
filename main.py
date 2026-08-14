
def auto_launch(url):
    import subprocess
    try:
        subprocess.run(['termux-open-url', url], check=False)
    except Exception:
        pass

import os
import time
import threading
import subprocess
import webbrowser
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from predictor import RacePredictor
from ai_analyst import AIAnalyst

app = Flask(__name__, static_folder='.')
CORS(app)

predictor = RacePredictor()
analyst = AIAnalyst()

# Global memory state for live race updates
LIVE_RACE_CACHE = {
    "last_updated": None,
    "race_info": {},
    "predictions": [],
    "analysis": []
}

def fetch_live_race_data():
    """
    Simulates / triggers live race card updates.
    Replace sample_live_card with your real web-scraper logic (e.g. BeautifulSoup/requests).
    """
    global LIVE_RACE_CACHE
    while True:
        try:
            # Example structure: replace with your live race scraper function
            sample_live_card = {
                "race_name": "Live Upcoming Race",
                "runners": [
                    {"name": "Runner A", "rating": 85, "form": 88, "weight": 60.0},
                    {"name": "Runner B", "rating": 78, "form": 80, "weight": 58.5},
                    {"name": "Runner C", "rating": 90, "form": 92, "weight": 61.5},
                    {"name": "Runner D", "rating": 70, "form": 65, "weight": 56.0}
                ]
            }

            runners = sample_live_card.get("runners", [])
            predictions = predictor.calculate_probabilities(runners)

            formatted_analysis = []
            for r in predictions:
                try:
                    prob_val = float(r["win_prob"].replace('%', ''))
                except ValueError:
                    prob_val = 0.0
                formatted_analysis.append({"name": r["runner"], "score": prob_val * 2})

            analysis = analyst.analyze_race(formatted_analysis)

            # Update live cache in memory
            LIVE_RACE_CACHE = {
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "race_name": sample_live_card.get("race_name"),
                "predictions": predictions,
                "analysis": analysis
            }
        except Exception as e:
            print(f"Error updating live race data: {e}")

        # Refresh predictions automatically every 60 seconds
        time.sleep(60)

# Serve Frontend
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Live Endpoint hit by index.html automatically
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        if 'predictor' in globals():
            data = predictor.get_live_predictions()
        elif 'RacePredictor' in globals():
            engine = RacePredictor()
            data = engine.get_live_predictions()
        else:
            from predictor import RacePredictor
            engine = RacePredictor()
            data = engine.get_live_predictions()
        return jsonify({'status': 'Active', 'live_data': data})
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))
    
    # Start live prediction engine worker thread
    threading.Thread(target=fetch_live_race_data, daemon=True).start()
    
    # Auto-open browser
    threading.Timer(1.5, auto_launch, args=[f"http://127.0.0.1:{port}/"]).start()
    
    app.run(host='0.0.0.0', port=port)
