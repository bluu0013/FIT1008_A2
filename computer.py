from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Computer:

    name: str
    hacking_difficulty: int
    hacked_value: int
    risk_factor: float

    def __lt__(self,other):
        if self.hacking_difficulty == other.hacking_difficulty:
            if self.risk_factor == other.risk_factor:
                return self.name < other.name
            else:
                return self.risk_factor < other.risk_factor
        else:
            return self.hacking_difficulty < other.hacking_difficulty
    
    def __gt__(self,other):
        if self.hacking_difficulty == other.hacking_difficulty:
            if self.risk_factor == other.risk_factor:
                return self.name < other.name
            else:
                return self.risk_factor > other.risk_factor
        else:
            return self.hacking_difficulty > other.hacking_difficulty
        
    def __le__(self,other):
        if self.hacking_difficulty == other.hacking_difficulty:
            if self.risk_factor == other.risk_factor:
                return self.name <= other.name
            else:
                return self.risk_factor <= other.risk_factor
        else:
            return self.hacking_difficulty <= other.hacking_difficulty

    def __ge__(self,other):
        if self.hacking_difficulty == other.hacking_difficulty:
            if self.risk_factor == other.risk_factor:
                return self.name >= other.name
            else:
                return self.risk_factor >= other.risk_factor
        else:
            return self.hacking_difficulty >= other.hacking_difficulty
           
    def __eq__(self,other):
        return (self.name == other.name)