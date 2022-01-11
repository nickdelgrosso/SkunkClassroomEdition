import random
from pytest import mark, raises

from models import DiceRoll

cases = [
    (1, 5, 6),
    (2, 3, 5),
]


@mark.parametrize("roll1,roll2,total", cases)
def test_can_calculate_sum_of_paired_d6_rolls(roll1, roll2, total):
    roll = DiceRoll(roll1=roll1, roll2=roll2)
    assert roll.sum() == total


cases = [(0, 5), (5, 0), (7, 6), (2, 7)]


@mark.parametrize("roll1,roll2", cases)
def test_nond6_values_raise_valueerror(roll1, roll2):
    with raises(ValueError):
        DiceRoll(roll1=roll1, roll2=roll2)


def test_generate_random_dice_pair_always_same_with_seed():
    roll1 = DiceRoll.new(seed=1)
    roll2 = DiceRoll.new(seed=1)
    assert roll1 == roll2
    roll3 = DiceRoll.new(seed=5)
    assert roll1 != roll3
    roll4 = DiceRoll.new(seed=4)
    assert roll1 != roll4
    assert roll3 != roll4


