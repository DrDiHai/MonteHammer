from abc import ABC, abstractmethod
from combatants.combatant import Combatant


class RollEvaluationStrategy(ABC):
    """Abstract base class for all saving throw strategies."""

    @abstractmethod
    def evaluate_roll(self, attacker: Combatant, target: Combatant, roll: int) -> bool:
        """Determine if the attacker hits the target based on the roll."""

    @abstractmethod
    def get_target_number(self, attacker: Combatant, target: Combatant) -> int:
        """Calculate the target number based on the attacker and target."""
