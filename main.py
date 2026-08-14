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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
