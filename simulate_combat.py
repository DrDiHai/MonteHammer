from combatants.unit import Combatant
from combat_result import CombatResult
from combatant_roll_evaluator.combatant_roll_evaluator import (
    Hit,
    HitWound,
    ArmourSave,
    WardSave,
    RegenerationSave,
)

SAMPLESIZE = 10000


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
