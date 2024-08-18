import json
from combatants.unit import Unit
from simulate_combat import simulate_combat

TIE_THRESHOLD = 0.05

if __name__ == "__main__":
    with open("units.json", encoding="utf-8") as file:
        data = json.load(file)
        units = [Unit.from_json(unit_data) for unit_data in data["units"]]

    for unit in units:
        print(unit)

    for i, attacker in enumerate(units):
        for j, target in enumerate(units):
            if i < j:  # Ensure each pairing is only considered once
                # Simulate combat with attacker attacking target
                attacker_results = simulate_combat(attacker, target)
                attacker_efficiency = (
                    attacker_results.kill_rate
                    * (target._points / attacker._points)
                    * 100
                )

                # Simulate combat with target attacking attacker
                target_results = simulate_combat(target, attacker)
                target_efficiency = (
                    target_results.kill_rate * (attacker._points / target._points) * 100
                )

                advantage_ratio = attacker_efficiency / target_efficiency

                # Determine the winner with a tie threshold
                if abs(advantage_ratio - 1) <= TIE_THRESHOLD:
                    winner = "🤝 It's a TIE! 🤝"
                elif advantage_ratio > 1:
                    winner = f"🏆 {attacker.get_name()} WINS! 🏆"
                else:
                    winner = f"🏆 {target.get_name()} WINS! 🏆"

                # Print results for both combat scenarios
                print(f"\n{'='*60}")
                print(
                    f"Combat Simulation: {attacker.get_name()} vs {target.get_name()}"
                )
                print(f"{'-'*60}")
                print(f"{attacker.get_name()} attacking {target.get_name()}:")
                print(f"  Hit Rate          : {attacker_results.hit_rate:.2f}")
                print(
                    f"  Wound Rate        : {attacker_results.wound_rate:.2f} (Raw: {attacker_results.raw_wound_rate:.2f})"
                )
                print(
                    f"  Unsaved Rate      : {attacker_results.unsaved_rate:.2f} (Raw: {attacker_results.raw_unsaved_rate:.2f})"
                )
                print(
                    f"  Unwarded Rate     : {attacker_results.unwarded_rate:.2f} (Raw: {attacker_results.raw_unwarded_rate:.2f})"
                )
                print(
                    f"  Unregenerated Rate: {attacker_results.unregenerated_rate:.2f} (Raw: {attacker_results.raw_unregenerated_rate:.2f})"
                )
                print(f"{'-'*60}")
                print(f"{target.get_name()} attacking {attacker.get_name()}:")
                print(f"  Hit Rate          : {target_results.hit_rate:.2f}")
                print(
                    f"  Wound Rate        : {target_results.wound_rate:.2f} (Raw: {target_results.raw_wound_rate:.2f})"
                )
                print(
                    f"  Unsaved Rate      : {target_results.unsaved_rate:.2f} (Raw: {target_results.raw_unsaved_rate:.2f})"
                )
                print(
                    f"  Unwarded Rate     : {target_results.unwarded_rate:.2f} (Raw: {target_results.raw_unwarded_rate:.2f})"
                )
                print(
                    f"  Unregenerated Rate: {target_results.unregenerated_rate:.2f} (Raw: {target_results.raw_unregenerated_rate:.2f})"
                )
                print(
                    f"Advantage {attacker.get_name()} ({attacker._points} points) vs. {target.get_name()} ({target._points} points): {advantage_ratio:.1f}"
                )
                print(f"{'-'*60}")
                print(f"{winner.center(58)}")
                print(f"{'='*60}\n")
