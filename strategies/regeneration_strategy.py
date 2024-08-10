"""This module contains the HitStrategy class and its subclasses."""

from abc import ABC, abstractmethod
from combatants.combatant import Combatant


class RegenerationStrategy(ABC):
    """Abstract base class for all saving throw strategies."""

    @abstractmethod
    def calculate_regen(
        self, attacker: Combatant, target: Combatant, roll: int
    ) -> bool:
        """Determine if the attacker hits the target based on the roll."""


class DefaultRegenerationStrategy(RegenerationStrategy):
    """Default saving throw strategy that pierces the targets armor on a roll of 1."""

    def calculate_regen(
        self, attacker: Combatant, target: Combatant, roll: int
    ) -> bool:
        """Calculate if the roll hits based on the modified roll."""
        target_number = self.get_target_number()
        return roll >= target_number

    def get_target_number(self) -> int:
        """Calculate the target number based on weapon skills."""
        return 1
