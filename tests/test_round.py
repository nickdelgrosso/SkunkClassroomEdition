from pytest import raises

from models import DiceRoll, Player, Round


def test_round_logs_roll_history():
    round = Round.new()

    roll = DiceRoll(roll1=2, roll2=3)
    round.add_roll(roll)
    round.add_roll(roll)
    round.add_roll(roll)
    assert len(round.rolls) == 3


def test_round_calculates_score_with_lockins():
    
    
    round = Round.new()
    players = [
        Player(name="Nick"),
        Player(name="Mary"),
        Player(name="Joe")
    ]
    for player in players:
        round.add_player(player)

    # roll1: 5
    roll = DiceRoll(roll1=2, roll2=3)
    round.add_roll(roll)
    scores = round.scores
    assert scores[players[0]] == 5
    assert scores[players[1]] == 5
    assert scores[players[2]] == 5

    # roll2: 11
    roll = DiceRoll(roll1=5, roll2=6)
    round.add_roll(roll)
    scores = round.scores
    assert scores[players[0]] == 16
    assert scores[players[1]] == 16
    assert scores[players[2]] == 16

    # player2 locks in, scores don't change
    round.add_lockin(players[1])
    scores = round.scores
    assert scores[players[0]] == 16
    assert scores[players[1]] == 16
    assert scores[players[2]] == 16

    # roll3: 4
    roll = DiceRoll(roll1=2, roll2=2)
    round.add_roll(roll)
    scores = round.scores
    assert scores[players[0]] == 20
    assert scores[players[1]] == 16
    assert scores[players[2]] == 20

    # player1 locks in
    round.add_lockin(players[0])

    # roll4: 7
    roll = DiceRoll(roll1=3, roll2=4)
    round.add_roll(roll)
    scores = round.scores
    assert scores[players[0]] == 20
    assert scores[players[1]] == 16
    assert scores[players[2]] == 27
    assert len(round.rolls) == 4

    # roll5: Skunk
    roll = DiceRoll(roll1=6, roll2=1)
    round.add_roll(roll)
    scores = round.scores
    assert scores[players[0]] == 20
    assert scores[players[1]] == 16
    assert scores[players[2]] == 0
    assert len(round.rolls) == 5

    # another roll not possible
    roll = DiceRoll(roll1=6, roll2=2)
    with raises(Exception):
        round.add_roll(roll)
    assert len(round.rolls) == 5


def test_late_players_get_same_number_of_points_as_everyone_else():
    round = Round.new()
    normal_player = Player(name='Nick')
    round.add_player(normal_player)
    round.add_roll(DiceRoll(roll1=5, roll2=6))
    assert round.scores[normal_player] == 11

    late_player = Player(name='John')
    round.add_player(late_player)
    assert round.scores[normal_player] == 11
    assert round.scores[late_player] == 11

    

