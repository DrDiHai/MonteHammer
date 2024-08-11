import json
from combatants.unit import Unit
from combatant_roll_evaluator.combatant_roll_evaluator import (
    Hit,
    HitWound,
    ArmourSave,
    RegenerationSave,
)

SAMPLESIZE = 10000


if __name__ == "__main__":
    with open("units.json", encoding="utf-8") as file:
        data = json.load(file)
        units = [Unit.from_json(unit_data) for unit_data in data["units"]]

    for unit in units:
        print(unit)

    for attacker in units:
        for target in units:
            hits = 0
            wounds = 0
            unsaved_wounds = 0
            unregenerated_wounds = 0
            for _ in range(SAMPLESIZE):
                hit = Hit(attacker, target)
                if hit.evaluate_roll():
                    hits += 1
                wound = HitWound(attacker, target)
                if wound.evaluate_roll():
                    wounds += 1
                armour_save = ArmourSave(attacker, target)
                if armour_save.evaluate_roll():
                    unsaved_wounds += 1
                regeneration_save = RegenerationSave(attacker, target)
                if regeneration_save.evaluate_roll():
                    unregenerated_wounds += 1
            attacks = attacker.get_attacks()
            hit_rate = (hits / SAMPLESIZE) * attacks
            raw_wound_rate = wounds / SAMPLESIZE
            wound_rate = ((wounds * hits) / (SAMPLESIZE * SAMPLESIZE)) * attacks
            raw_unsaved_rate = unsaved_wounds / SAMPLESIZE
            unsaved_rate = (
                (wounds * hits * unsaved_wounds)
                / (SAMPLESIZE * SAMPLESIZE * SAMPLESIZE)
            ) * attacks
            raw_unregenerated_rate = unregenerated_wounds / SAMPLESIZE
            unregenerated_rate = (
                (wounds * hits * unsaved_wounds * unregenerated_wounds)
                / (SAMPLESIZE * SAMPLESIZE * SAMPLESIZE * SAMPLESIZE)
            ) * attacks

            # Calculate the efficiency

            survival_rate = unregenerated_rate / target._wounds
            destroyed_points = survival_rate * target._points
            deployed_points = attacker._points  # Dynamically added cost from JSON
            efficiency = (
                destroyed_points / deployed_points
            ) * 100  # Added * 100 for better readability

            # Improved print statement for better readability and efficiency display
            print(f"\n{'='*60}")
            print(f"Combat Simulation: {attacker.get_name()} vs {target.get_name()}")
            print(f"{'-'*60}")
            print(f"Total Attacks: {attacks}")
            print(f"Hit Rate          : {hit_rate:.2f}")
            print(f"Wound Rate        : {wound_rate:.2f} (Raw: {raw_wound_rate:.2f})")
            print(
                f"Unsaved Rate      : {unsaved_rate:.2f} (Raw: {raw_unsaved_rate:.2f})"
            )
            print(
                f"Unregenerated Rate: {unregenerated_rate:.2f} (Raw: {raw_unregenerated_rate:.2f})"
            )
            print(f"Efficiency        : {efficiency:.5f} per point cost")
            print(f"{'='*60}\n")
