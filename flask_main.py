from flask import Flask, jsonify, request
import json
from main import simulate_combat
from combatants.unit import Unit

# Assuming SAMPLESIZE and other related functions are defined elsewhere
SAMPLESIZE = 10000
TIE_THRESHOLD = 0.05  # 5% threshold for declaring a tie

app = Flask(__name__)

# Load units from JSON file
with open("units.json", encoding="utf-8") as file:
    units_data = json.load(file)
    units = [Unit.from_json(unit_data) for unit_data in units_data["units"]]

# Create a dictionary for easy lookup by name
units_dict = {unit.get_name(): unit for unit in units}


@app.route("/evaluate", methods=["GET"])
def evaluate_units():
    # Get unit names from query parameters
    attacker_name = request.args.get("attacker")
    target_name = request.args.get("target")

    # Check if both units exist
    if attacker_name not in units_dict or target_name not in units_dict:
        return jsonify({"error": "One or both units not found"}), 404

    attacker = units_dict[attacker_name]
    target = units_dict[target_name]

    # Simulate combat between the units
    attacker_results = simulate_combat(attacker, target)
    attacker_efficiency = (
        attacker_results.kill_rate * (target._points / attacker._points) * 100
    )
    target_results = simulate_combat(target, attacker)
    target_efficiency = (
        target_results.kill_rate * (attacker._points / target._points) * 100
    )
    advantage_ratio = attacker_efficiency / target_efficiency

    # Determine winner
    if abs(advantage_ratio - 1) <= TIE_THRESHOLD:
        winner = "It's a TIE!"
    elif advantage_ratio > 1:
        winner = f"{attacker_name} WINS!"
    else:
        winner = f"{target_name} WINS!"

    # Return results as JSON
    return jsonify(
        {
            "attacker": attacker_name,
            "attacker_points": attacker._points,
            "target": target_name,
            "target_points": target._points,
            "advantage_ratio": round(advantage_ratio, 2),
            "winner": winner,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
