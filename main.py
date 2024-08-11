import json
from combatants.combatant import Combatant
from combatants.unit import Unit
from combat_result import CombatResult
from combatant_roll_evaluator.combatant_roll_evaluator import (
    Hit,
    HitWound,
    ArmourSave,
    WardSave,
    RegenerationSave,
)

SAMPLESIZE = 10000
TIE_THRESHOLD = 0.05


def simulate_combat(attacking_combatant: Combatant, target_combatant: Combatant):
    hits = 0
    wounds = 0
    unsaved_wounds = 0
    unwarded_wounds = 0
    unregenerated_wounds = 0

    for _ in range(SAMPLESIZE):
        hit = Hit(attacking_combatant, target_combatant)
        if hit.evaluate_roll():
            hits += 1
        wound = HitWound(attacking_combatant, target_combatant)
        if wound.evaluate_roll():
            wounds += 1
        armour_save = ArmourSave(attacking_combatant, target_combatant)
        if armour_save.evaluate_roll():
            unsaved_wounds += 1
        ward_save = WardSave(attacking_combatant, target_combatant)
        if ward_save.evaluate_roll():
            unwarded_wounds += 1
        regeneration_save = RegenerationSave(attacking_combatant, target_combatant)
        if regeneration_save.evaluate_roll():
            unregenerated_wounds += 1

    attacks = attacking_combatant.get_attacks()
    hit_rate = (hits / SAMPLESIZE) * attacks
    raw_wound_rate = wounds / SAMPLESIZE
    wound_rate = ((wounds * hits) / (SAMPLESIZE * SAMPLESIZE)) * attacks
    raw_unsaved_rate = unsaved_wounds / SAMPLESIZE
    unsaved_rate = (
        (wounds * hits * unsaved_wounds) / (SAMPLESIZE * SAMPLESIZE * SAMPLESIZE)
    ) * attacks
    raw_unwarded_rate = unwarded_wounds / SAMPLESIZE
    unwarded_rate = (
        (wounds * hits * unsaved_wounds * unwarded_wounds)
        / (SAMPLESIZE * SAMPLESIZE * SAMPLESIZE * SAMPLESIZE)
    ) * attacks
    raw_unregenerated_rate = unregenerated_wounds / SAMPLESIZE
    unregenerated_rate = (
        (wounds * hits * unsaved_wounds * unwarded_wounds * unregenerated_wounds)
        / (SAMPLESIZE * SAMPLESIZE * SAMPLESIZE * SAMPLESIZE * SAMPLESIZE)
    ) * attacks

    kill_rate = unregenerated_rate / target_combatant._wounds

    return CombatResult(
        hit_rate,
        raw_wound_rate,
        wound_rate,
        raw_unsaved_rate,
        unsaved_rate,
        raw_unwarded_rate,
        unwarded_rate,
        raw_unregenerated_rate,
        unregenerated_rate,
        kill_rate,
    )


if __name__ == "__main__":
    with open("units.json", encoding="utf-8") as file:
        data = json.load(file)
        units = [Unit.from_json(unit_data) for unit_data in data["units"]]

    for unit in units:
        print(unit)

    for i, attacker in enumerate(units):
        for j, target in enumerate(units):
            if i <= j:  # Ensure each pairing is only considered once
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
