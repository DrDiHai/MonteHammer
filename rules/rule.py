from abc import abstractmethod
from combatants.combatant import Combatant
from rules.modifier import Modifier


class Rule(Modifier):
    """Abstract base class for all rules."""


class RollModifierRule(Rule):

    @abstractmethod
    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the specific modifier's rules."""


class HitRollModifier(RollModifierRule):
    pass


class RerollModifierRule(Rule):
    """Abstract base class for all rules to determine if a reroll should be granted."""

    @abstractmethod
    def should_reroll(self, roll: int, attacker: Combatant, target: Combatant) -> bool:
        """Determine if a reroll should be granted."""


class HitRerollModifier(RerollModifierRule):
    pass


class WoundRollModifier(RollModifierRule):
    pass


class WoundRerollModifier(RerollModifierRule):
    pass


class SaveRollModifier(RollModifierRule):
    pass


class SaveRerollModifier(RerollModifierRule):
    pass


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


class ArmourPiercing(SaveRollModifier):
    """Represents the AP characteristic of a weapon or rule."""

    def __init__(self, modifier: int):
        assert 1 <= modifier <= 6
        self._modifier = modifier

    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the regeneration save rules."""
        return roll + self._modifier


class WardSaveRollModifier(RollModifierRule):
    pass


class WardSaveRerollModifier(RerollModifierRule):
    pass


class RegenerationSaveRollModifier(RollModifierRule):
    pass


class RegenerationSaveRerollModifier(RerollModifierRule):
    pass


class RegenerationSave(RegenerationSaveRollModifier):
    """Rule to modify the target's regeneration save."""

    def __init__(self, threshold: int):
        assert 1 <= threshold <= 6
        self._threshold = threshold

    def modify_roll(self, roll: int, attacker: Combatant, target: Combatant) -> int:
        """Modify the roll based on the regeneration save rules."""
        return roll - (self._threshold - 5)
