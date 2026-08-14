"""
[THE CARD // AI CO-PILOT]
Synthesizes raw heuristic outputs with contextual reasoning to flag 
value bets, track biases, and hidden risk factors.
"""

class AIAnalyst:
    def __init__(self, model_name="The Card Core"):
        self.model_name = model_name

    def critique_field(self, race_title, evaluated_runners, track_conditions):
        top_pick = evaluated_runners[0]
        value_shouts = [r for r in evaluated_runners if r['predicted_rating'] > 7.0]
        
        print(f"\n🧠 [{self.model_name}] Analyzing Race Context: {race_title}")
        print(f"--------------------------------------------------")
        print(f"🏟️ Track Condition: {track_conditions.get('going', 'Good')} | Rail: {track_conditions.get('rail', 'True')} | Distance: {track_conditions.get('distance', 1200)}m")
        print(f"🏆 Top Computer Selection: #{top_pick['draw']} {top_pick['horse_name']} (Score: {top_pick['predicted_rating']})")
        
        insights = []
        if top_pick['draw'] > 8 and track_conditions.get('distance', 1200) <= 1400:
            insights.append("⚠️ Warning: Top pick carries a wide draw on a sharp layout; tactical risk is high.")
        
        if len(value_shouts) > 1:
            insights.append(f"💡 Value Alert: Multiple runners showing strong convergent metrics ({len(value_shouts)} contenders clear threshold). Look at exacta/swinger combinations.")
        else:
            insights.append("🔒 Single-heavy race structure. The metrics heavily favor the top selection.")
            
        return insights
