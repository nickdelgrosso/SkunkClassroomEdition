from __future__ import annotations

import random
from typing import Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DiceRoll:
    roll1: int
    roll2: int

    def __post_init__(self):
        try:
            assert 1 <= self.roll1 <= 6
            assert 1 <= self.roll2 <= 6
        except AssertionError:
            raise ValueError(f"both rolls must be between 1 and 6")

    def sum(self):
        return self.roll1 + self.roll2

    @classmethod
    def new(cls, seed: Optional[int] = None) -> DiceRoll:
        randomizer = random.Random() if seed is None else random.Random(seed)
        diceroll = DiceRoll(
            roll1=randomizer.randint(1, 6), roll2=randomizer.randint(1, 6)
        )
        return diceroll

