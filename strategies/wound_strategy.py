"""This module contains the HitStrategy class and its subclasses."""

from abc import ABC, abstractmethod
from combatants.combatant import Combatant


class WoundStrategy(ABC):
    """Abstract base class for all hit strategies."""

    @abstractmethod
    def calculate_wound(
        self, attacker: Combatant, target: Combatant, roll: int
    ) -> bool:
        """Determine if the attacker hits the target based on the roll."""


class DefaultWoundStrategy(WoundStrategy):
    """Default hit strategy that uses the attacker's and target's weapon skill to calculate the target number."""

    def calculate_wound(
        self, attacker: Combatant, target: Combatant, roll: int
    ) -> bool:
        """Calculate if the roll hits based on the modified roll."""
        target_number = self.get_target_number(attacker, target)
        return roll >= target_number

    def get_target_number(self, attacker: Combatant, target: Combatant) -> int:
        """Calculate the target number based on weapon skills."""
        target_number = 5
        attacker_strength = attacker.get_strength()
        target_toughness = target.get_toughness()

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
