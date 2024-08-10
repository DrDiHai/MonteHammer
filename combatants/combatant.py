# combatant.py

from abc import ABC, abstractmethod
from rules.modifier import Modifier


class Combatant(ABC):
    @abstractmethod
    def get_weapon_skill(self) -> int:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_strength(self) -> int:
        pass

    @abstractmethod
    def get_toughness(self) -> int:
        pass

    @abstractmethod
    def get_initiative(self) -> int:
        pass

    @abstractmethod
    def get_attacks(self) -> int:
        pass

    @abstractmethod
    def get_defensive_modifiers(self) -> list[Modifier]:
        pass

    @abstractmethod
    def get_offensive_modifiers(self) -> list[Modifier]:
        pass

    # Add other methods that might be needed by the strategy
