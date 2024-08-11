"""This module contains the HitStrategy class and its subclasses."""

from strategies.roll_evaluation_strategy import RollEvaluationStrategy
from combatants.combatant import Combatant


class DefaultWardStrategy(RollEvaluationStrategy):
    """Default saving throw strategy that pierces the targets ward on a roll of 1."""

    def evaluate_roll(self, attacker: Combatant, target: Combatant, roll: int) -> bool:
        """Calculate if the roll hits based on the modified roll."""
        target_number = self.get_target_number()
        return roll >= target_number

    def get_target_number(self) -> int:
        """Calculate the target number based on weapon skills."""
        return 1
