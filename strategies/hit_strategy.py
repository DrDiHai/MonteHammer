"""This module contains the HitStrategy class and its subclasses."""

from abc import ABC, abstractmethod
from combatants.combatant import Combatant


class HitStrategy(ABC):
    """Abstract base class for all hit strategies."""

    @abstractmethod
    def calculate_hit(self, attacker: Combatant, target: Combatant, roll: int) -> bool:
        """Determine if the attacker hits the target based on the roll."""


class DefaultHitStrategy(HitStrategy):
    """Default hit strategy that uses the attacker's and target's weapon skill to calculate the target number."""

    def calculate_hit(self, attacker: Combatant, target: Combatant, roll: int) -> bool:
        """Calculate if the roll hits based on the modified roll."""
        target_number = self.get_target_number(attacker, target)
        return roll >= target_number

    def get_target_number(self, attacker: Combatant, target: Combatant) -> int:
        """Calculate the target number based on weapon skills."""
        target_number = 5
        attacker_skill = attacker.get_weapon_skill()
        target_skill = target.get_weapon_skill()

        if target_skill <= attacker_skill * 2:
            target_number = 4
        if target_skill < attacker_skill:
            target_number = 3
        if target_skill < attacker_skill / 2:
            target_number = 2

        return target_number
