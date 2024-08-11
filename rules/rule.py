from abc import abstractmethod
from random import randint
from combatants.combatant import Combatant
from strategies.roll_evaluation_strategy import RollEvaluationStrategy
from rules.modifier import Modifier


class Rule(Modifier):
    """Abstract base class for all rules."""


class AutoSuccessModifierRule(Rule):
    """Abstract base class for all rules that determine if a roll is an automatic success."""

    @abstractmethod
    def is_auto_success(self, attacker: Combatant, target: Combatant) -> bool:
        """Determine if the roll is an automatic success."""


class AutoHitModifier(AutoSuccessModifierRule):
    pass


class AutoWoundModifier(AutoSuccessModifierRule):
    pass


class AutoPenetrateArmourModifier(AutoSuccessModifierRule):

    def is_auto_success(self, attacker: Combatant, target: Combatant) -> bool:
        pass


class AutoPenetrateWardModifier(AutoSuccessModifierRule):
    pass


class AutoPenetrateRegenerationModifier(AutoSuccessModifierRule):
    pass


class CleavingBlow(AutoPenetrateArmourModifier, AutoPenetrateRegenerationModifier):

    def is_auto_success(self, attacker: Combatant, target: Combatant) -> bool:
        # TODO: Check for unit type

        wound_strategy: RollEvaluationStrategy = attacker._wound_strategy
        roll_lower_bound = wound_strategy.get_target_number(attacker, target)
        return randint(roll_lower_bound, 6) == 6


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
