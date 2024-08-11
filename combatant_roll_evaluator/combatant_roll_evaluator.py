"""This module contains the Hit class, which is responsible for determining if
an attacker hits a target."""

from combatants.combatant import Combatant
from dieroll import rolld6
from strategies.roll_evaluation_strategy import RollEvaluationStrategy
from rules.rule import RollModifierRule, RerollModifierRule
from rules.rule import HitRollModifier, HitRerollModifier
from rules.rule import WoundRollModifier, WoundRerollModifier
from rules.rule import SaveRollModifier, SaveRerollModifier
from rules.rule import WardSaveRollModifier, WardSaveRerollModifier
from rules.rule import RegenerationSaveRollModifier, RegenerationSaveRerollModifier


class CombatantRollEvaluator:
    """Base class for evaluating combatant rolls."""

    def __init__(
        self,
        attacker: Combatant,
        target: Combatant,
        roll_modifier_class: RollModifierRule,
        reroll_modifier_class: RerollModifierRule,
        strategy_name: str,
    ):
        self._attacker = attacker
        self._target = target
        self._roll_modifiers: list[RollModifierRule] = []
        self._reroll_modifiers: list[RerollModifierRule] = []

        # Retrieve strategy and modifiers from the attacker
        self._strategy: RollEvaluationStrategy = getattr(attacker, strategy_name)

        # Combine roll modifiers from both attacker and target
        self._roll_modifiers = [
            m
            for m in attacker.get_offensive_modifiers()
            if isinstance(m, roll_modifier_class)
        ] + [
            m
            for m in target.get_defensive_modifiers()
            if isinstance(m, roll_modifier_class)
        ]

        # Combine reroll modifiers from both attacker and target
        self._reroll_modifiers = [
            m
            for m in attacker.get_offensive_modifiers()
            if isinstance(m, reroll_modifier_class)
        ] + [
            m
            for m in target.get_defensive_modifiers()
            if isinstance(m, reroll_modifier_class)
        ]

    def evaluate_roll(self) -> bool:
        """Determine if the attacker hits the target, applying modifiers
        and allowing only one reroll."""
        # Perform the roll, apply modifiers, and check for hit
        roll = self._roll_and_apply_modifiers()

        if self._strategy.evaluate_roll(self._attacker, self._target, roll):
            return True

        # If the initial roll failed, check if we should reroll
        if self._should_reroll(roll):
            roll = self._roll_and_apply_modifiers()
            return self._strategy.evaluate_roll(self._attacker, self._target, roll)

        return False

    def _roll_and_apply_modifiers(self) -> int:
        """Roll the die and apply all roll modifiers."""
        roll = rolld6()
        for modifier in self._roll_modifiers:
            roll = modifier.modify_roll(roll, self._attacker, self._target)
        return roll

    def _should_reroll(self, roll: int) -> bool:
        """Determine if a reroll should be performed based on reroll modifiers."""
        for reroll_modifier in self._reroll_modifiers:
            if reroll_modifier.should_reroll(roll, self._attacker, self._target):
                return True
        return False


class Hit(CombatantRollEvaluator):
    def __init__(self, attacker: Combatant, target: Combatant):
        super().__init__(
            attacker, target, HitRollModifier, HitRerollModifier, "_hit_strategy"
        )


class HitWound(CombatantRollEvaluator):
    def __init__(self, attacker: Combatant, target: Combatant):
        super().__init__(
            attacker, target, WoundRollModifier, WoundRerollModifier, "_wound_strategy"
        )


class ArmourSave(CombatantRollEvaluator):
    def __init__(self, attacker: Combatant, target: Combatant):
        super().__init__(
            attacker, target, SaveRollModifier, SaveRerollModifier, "_save_strategy"
        )


class WardSave(CombatantRollEvaluator):
    def __init__(self, attacker: Combatant, target: Combatant):
        super().__init__(
            attacker,
            target,
            WardSaveRollModifier,
            WardSaveRerollModifier,
            "_ward_strategy",
        )


class RegenerationSave(CombatantRollEvaluator):
    def __init__(self, attacker: Combatant, target: Combatant):
        super().__init__(
            attacker,
            target,
            RegenerationSaveRollModifier,
            RegenerationSaveRerollModifier,
            "_regeneration_strategy",
        )
