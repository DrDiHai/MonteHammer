import importlib
from typing import List, Optional, Any
from combatants.combatant import Combatant
from strategies.hit_strategy import HitStrategy
from strategies.wound_strategy import WoundStrategy
from strategies.save_strategy import SaveStrategy
from rules.modifier import Modifier


class Unit(Combatant):
    def __init__(
        self,
        **kwargs,  # Capture additional attributes
    ):
        self._hit_strategy: HitStrategy = None
        self._defensive_modifiers: List[Modifier] = []
        self._offensive_modifiers: List[Modifier] = []

        self._name: Optional[str] = None
        self._weapon_skill: Optional[int] = None
        self._ballistic_skill: Optional[int] = None
        self._strength: Optional[int] = None
        self._toughness: Optional[int] = None
        self._initiative: Optional[int] = None
        self._attacks: Optional[int] = None
        self._wounds: Optional[int] = None

        # Dynamically add any additional attributes from kwargs with underscore prefix
        for key, value in kwargs.items():
            setattr(self, f"_{key}", value)

    def __repr__(self) -> str:
        return f"Unit({self._name})"

    def __str__(self) -> str:
        return (
            f"Unit {self._name} with WS {self._weapon_skill}, BS {self._ballistic_skill}, "
            f"S {self._strength}, T {self._toughness}, I {self._initiative}, "
            f"A {self._attacks}, W {self._wounds}"
        )

    def get_name(self) -> Optional[str]:
        return self._name

    def get_weapon_skill(self) -> Optional[int]:
        return self._weapon_skill

    def get_strength(self) -> Optional[int]:
        return self._strength

    def get_toughness(self) -> Optional[int]:
        return self._toughness

    def get_initiative(self) -> Optional[int]:
        return self._initiative

    def get_attacks(self) -> Optional[int]:
        return self._attacks

    def calculate_damage(self, other_unit: "Unit") -> Any:
        """Calculate the damage this unit would deal to another unit using its strategy."""
        return self._hit_strategy.calculate_damage(self, other_unit)

    def set_hit_strategy(self, hit_strategy: HitStrategy) -> None:
        self._hit_strategy = hit_strategy

    def set_wound_strategy(self, wound_strategy: WoundStrategy) -> None:
        self._wound_strategy = wound_strategy

    def set_save_strategy(self, save_strategy: SaveStrategy) -> None:
        self._save_strategy = save_strategy

    def set_regeneration_strategy(self, regeneration_strategy: SaveStrategy) -> None:
        self._regeneration_strategy = regeneration_strategy

    def add_defensive_modifier(self, modifier: Modifier) -> None:
        if self._defensive_modifiers is None:
            self._defensive_modifiers = []
        self._defensive_modifiers.append(modifier)

    def get_defensive_modifiers(self) -> List[Modifier]:
        return self._defensive_modifiers

    def add_offensive_modifier(self, modifier: Modifier) -> None:
        if self._offensive_modifiers is None:
            self._offensive_modifiers = []
        self._offensive_modifiers.append(modifier)

    def get_offensive_modifiers(self) -> List[Modifier]:
        return self._offensive_modifiers

    @staticmethod
    def from_json(data: dict) -> "Unit":
        """Factory method to create a Unit from JSON data dynamically."""

        def load_class(module_name: str, class_name: str) -> Any:
            """Dynamically load a class from a string."""
            try:
                module = importlib.import_module(f"strategies.{module_name}")
            except ModuleNotFoundError:
                module = importlib.import_module(f"rules.{module_name}")
            return getattr(module, class_name)

        # Handle special cases: hit_strategy and modifiers
        hit_strategy_class_name = data.pop("hit_strategy", "DefaultHitStrategy")
        hit_strategy = load_class("hit_strategy", hit_strategy_class_name)()
        wound_strategy_class_name = data.pop("wound_strategy", "DefaultWoundStrategy")
        wound_strategy = load_class("wound_strategy", wound_strategy_class_name)()
        save_strategy_class_name = data.pop("save_strategy", "DefaultSaveStrategy")
        save_strategy = load_class("save_strategy", save_strategy_class_name)()
        regeneration_strategy_class_name = data.pop(
            "save_strategy", "DefaultRegenerationStrategy"
        )
        regeneration_strategy = load_class(
            "regeneration_strategy", regeneration_strategy_class_name
        )()

        defensiveModifiers = []
        for modifier_data in data.pop("defensiveModifiers", []):
            if isinstance(modifier_data, dict):
                # Assume the dict contains the class name and its parameters
                class_name = modifier_data.pop("class")
                modifier_class = load_class("rule", class_name)
                # Initialize with additional parameters
                modifier_instance = modifier_class(**modifier_data)
            else:
                # Just the class name with no additional parameters
                modifier_class = load_class("rule", modifier_data)
                modifier_instance = modifier_class()
            defensiveModifiers.append(modifier_instance)

        offensiveModifiers = []
        for modifier_data in data.pop("offensiveModifiers", []):
            if isinstance(modifier_data, dict):
                # Assume the dict contains the class name and its parameters
                class_name = modifier_data.pop("class")
                modifier_class = load_class("rule", class_name)
                # Initialize with additional parameters
                modifier_instance = modifier_class(**modifier_data)
            else:
                # Just the class name with no additional parameters
                modifier_class = load_class("rule", modifier_data)
                modifier_instance = modifier_class()
            offensiveModifiers.append(modifier_instance)

        # Create and return the Unit instance
        unit = Unit(
            **data,  # Pass the remaining attributes dynamically with underscore prefix
        )

        unit.set_hit_strategy(hit_strategy)
        unit.set_wound_strategy(wound_strategy)
        unit.set_save_strategy(save_strategy)
        unit.set_regeneration_strategy(regeneration_strategy)
        for modifier in defensiveModifiers:
            unit.add_defensive_modifier(modifier)
        for modifier in offensiveModifiers:
            unit.add_offensive_modifier(modifier)

        return unit
