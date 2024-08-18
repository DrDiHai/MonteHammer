"""This module contains the HitStrategy class and its subclasses."""

from strategies.roll_evaluation_strategy import RollEvaluationStrategy
from combatants.combatant import Combatant
from rules.rule import StrengthModifier, ToughnessModifier


class DefaultWoundStrategy(RollEvaluationStrategy):
    """Default hit strategy that uses the attacker's and target's weapon skill to calculate the target number."""

    def evaluate_roll(self, attacker: Combatant, target: Combatant, roll: int) -> bool:
        """Calculate if the roll hits based on the modified roll."""
        target_number = self.get_target_number(attacker, target)
        return roll >= target_number

    def get_target_number(self, attacker: Combatant, target: Combatant) -> int:
        """Calculate the target number based on attacker strength and target toughness."""
        attacker_strength = attacker.get_strength() + sum(
            [
                modifier.get_modifier(attacker)
                for modifier in attacker._offensive_modifiers
                if isinstance(modifier, StrengthModifier)
            ]
        )
        target_toughness = target.get_toughness() + sum(
            [
                modifier.get_modifier(target)
                for modifier in target._defensive_modifiers
                if isinstance(modifier, ToughnessModifier)
            ]
        )

        if target_toughness > attacker_strength + 5:
            return 7
        if target_toughness > attacker_strength + 1:
            return 6
        if target_toughness > attacker_strength:
            return 5
        if target_toughness == attacker_strength:
            return 4
        if target_toughness > attacker_strength - 2:
            return 3
        return 2
