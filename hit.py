"""This module contains the Hit class, which is responsible for determining if
an attacker hits a target."""

from combatants.combatant import Combatant
from dieroll import rolld6
from strategies.roll_evaluation_strategy import RollEvaluationStrategy
from rules.rule import HitRollModifier, HitRerollModifier


class Hit:
    def __init__(self, attacker: Combatant, target: Combatant):
        self._attacker = attacker
        self._target = target

        # Retrieve strategy and modifiers from the attacker
        self._strategy: RollEvaluationStrategy = attacker._hit_strategy

        # Combine roll modifiers from both attacker and target
        self._roll_modifiers = [
            m
            for m in attacker.get_offensive_modifiers()
            if isinstance(m, HitRollModifier)
        ] + [
            m
            for m in target.get_defensive_modifiers()
            if isinstance(m, HitRollModifier)
        ]

        # Combine reroll modifiers from both attacker and target
        self._reroll_modifiers = [
            m
            for m in attacker.get_offensive_modifiers()
            if isinstance(m, HitRerollModifier)
        ] + [
            m
            for m in target.get_defensive_modifiers()
            if isinstance(m, HitRerollModifier)
        ]

    def hit_target(self) -> bool:
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
