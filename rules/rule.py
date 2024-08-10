from abc import ABC, abstractmethod
from combatants.combatant import Combatant
from rules.modifier import Modifier


class Rule(Modifier):
    """Abstract base class for all rules."""


class HitRollModifier(Rule):
    """Abstract base class for all rules to modify dice rolls."""

    @abstractmethod
    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the specific modifier's rules."""


class HitRerollModifier(Rule):
    """Abstract base class for all rules to determine if a reroll should be granted."""

    @abstractmethod
    def should_reroll(self, roll: int, attacker: Combatant, target: Combatant) -> bool:
        """Determine if a reroll should be granted."""


class WoundRollModifier(Rule):
    """Abstract base class for all rules to modify dice rolls."""

    @abstractmethod
    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the specific modifier's rules."""


class WoundRerollModifier(Rule):
    """Abstract base class for all rules to determine if a reroll should be granted."""

    @abstractmethod
    def should_reroll(self, roll: int, attacker: Combatant, target: Combatant) -> bool:
        """Determine if a reroll should be granted."""


class SaveRollModifier(Rule):
    """Abstract base class for all rules to modify dice rolls."""

    @abstractmethod
    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the specific modifier's rules."""


class SaveRerollModifier(Rule):
    """Abstract base class for all rules to determine if a reroll should be granted."""

    @abstractmethod
    def should_reroll(self, roll: int, attacker: Combatant, target: Combatant) -> bool:
        """Determine if a reroll should be granted."""


class LightArmour(SaveRollModifier):
    """Rule to modify the target's armour save based on light armour."""

    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the light armour rules."""
        return roll - 1


class HeavyArmour(SaveRollModifier):
    """Rule to modify the target's armour save based on heavy armour."""

    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the heavy armour rules."""
        return roll - 2


class Shield(SaveRollModifier):
    """Rule to modify the target's armour save based on a shield."""

    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the shield rules."""
        return roll - 1


class WardSaveRollModifier(Rule):
    """Abstract base class for all rules to modify dice rolls."""

    @abstractmethod
    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the specific modifier's rules."""


class WardSaveRerollModifier(Rule):
    """Abstract base class for all rules to determine if a reroll should be granted."""

    @abstractmethod
    def should_reroll(self, roll: int, attacker: Combatant, target: Combatant) -> bool:
        """Determine if a reroll should be granted."""


class RegenerationSaveRollModifier(Rule):
    """Abstract base class for all rules to modify dice rolls."""

    @abstractmethod
    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the specific modifier's rules."""


class RegenerationSaveRerollModifier(Rule):
    """Abstract base class for all rules to determine if a reroll should be granted."""

    @abstractmethod
    def should_reroll(self, roll: int, attacker: Combatant, target: Combatant) -> bool:
        """Determine if a reroll should be granted."""


class RegenerationSave(RegenerationSaveRollModifier):
    """Rule to modify the target's regeneration save."""

    def __init__(self, threshold: int):
        assert 1 <= threshold <= 6
        self._threshold = threshold

    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the regeneration save rules."""
        return roll - (self._threshold - 5)
