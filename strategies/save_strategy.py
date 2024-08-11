"""This module contains the HitStrategy class and its subclasses."""

from strategies.roll_evaluation_strategy import RollEvaluationStrategy
from combatants.combatant import Combatant


class DefaultSaveStrategy(RollEvaluationStrategy):
    """Default saving throw strategy that pierces the targets armor on a roll of 1."""

    def evaluate_roll(self, attacker: Combatant, target: Combatant, roll: int) -> bool:
        target_number = self.get_target_number()
        return roll >= target_number

    def get_target_number(self) -> int:
        """Pierce an all rolls unless modified."""
        return 1
