"""
[THE CARD // PREDICTOR] Tactical Horse Racing Predictor
Pure Python implementation (No Pandas/Numpy heavy C-extensions required).
"""

class HorseRacePredictor:
    def __init__(self):
        print("🐴 [THE CARD // PREDICTOR] Initializing lightweight algorithmic race matrix...")

    def evaluate_field(self, race_card_data):
        scored_runners = []
        distance = race_card_data.get("distance", 1200)
        
        for horse in race_card_data.get("runners", []):
            form_score = self._calculate_form(horse.get("past_results", []))
            weight_score = self._evaluate_weight(horse.get("weight", 55.0))
            draw_score = self._evaluate_draw(horse.get("draw", 1), distance)
            
            total_score = (form_score * 0.4) + (weight_score * 0.2) + (draw_score * 0.2) + (0.2 * 5.0)
            
            scored_runners.append({
                "horse_name": horse.get("name"),
                "draw": horse.get("draw"),
                "weight": horse.get("weight"),
                "predicted_rating": round(total_score, 2)
            })
            
        scored_runners.sort(key=lambda x: x["predicted_rating"], reverse=True)
        return scored_runners

    def _calculate_form(self, results):
        if not results:
            return 5.0
        points = {1: 10, 2: 7, 3: 5, 4: 3}
        score = sum([points.get(pos, 1) for pos in results[:5]]) / min(len(results), 5)
        return min(max(score, 1.0), 10.0)

    def _evaluate_weight(self, weight):
        if 54.0 <= weight <= 58.0:
            return 8.0
        return 5.0

    def _evaluate_draw(self, draw, distance):
        if distance <= 1400 and draw <= 4:
            return 9.0
        return 6.0
