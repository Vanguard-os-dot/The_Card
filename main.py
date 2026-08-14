"""
[THE CARD] Local Execution Entrypoint
"""
from orby_core.horse_predictor import HorseRacePredictor
from orby_core.ai_analyst import AIAnalyst

def run_local_simulation():
    print("🚀 Booting up THE CARD local race desk...")
    
    predictor = HorseRacePredictor()
    analyst = AIAnalyst()
    
    sample_card = {
        "track": "Turffontein",
        "distance": 1200,
        "runners": [
            {"name": "Lightning Bolt", "draw": 2, "weight": 56.5, "past_results": [1, 2, 1, 4]},
            {"name": "Ironclad", "draw": 8, "weight": 58.0, "past_results": [3, 1, 5, 2]},
            {"name": "Shadow Dancer", "draw": 1, "weight": 54.0, "past_results": [2, 3, 2, 1]}
        ]
    }
    
    conditions = {
        "going": "Good",
        "rail": "3m out on bend",
        "distance": sample_card["distance"]
    }
    
    results = predictor.evaluate_field(sample_card)
    
    print("\n🎯 Final Predicted Ratings Matrix:")
    for idx, r in enumerate(results, 1):
        print(f"#{idx}: {r['horse_name']} (Draw: {r['draw']}, Wt: {r['weight']}kg) - Score: {r['predicted_rating']}")
        
    notes = analyst.critique_field(f"{sample_card['track']} Sprint - {sample_card['distance']}m", results, conditions)
    for note in notes:
        print(note)

if __name__ == "__main__":
    run_local_simulation()
