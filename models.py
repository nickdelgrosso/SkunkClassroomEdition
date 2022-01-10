from __future__ import annotations


import random
from typing import Dict, Optional, List, Set, Tuple, Union, final
from uuid import uuid4
from pydantic import BaseModel, Field, validator



class DiceRoll(BaseModel):
    roll1: int
    roll2: int

    @validator('roll1', 'roll2', allow_reuse=True)
    def val_from_1_to_6(cls, roll):
        if not 1 <= roll <= 6:
            raise ValueError("roll must be between 1 and 6")
        return roll

    def sum(self):
        return self.roll1 + self.roll2

    @classmethod
    def new(cls, seed: Optional[int] = None) -> DiceRoll:
        randomizer = random.Random() if seed is None else random.Random(seed)
        diceroll = DiceRoll(
            roll1=randomizer.randint(1, 6), roll2=randomizer.randint(1, 6)
        )
        return diceroll

    def is_skunk(self) -> bool:
        return self.roll1 == 1 or self.roll2 == 1

    def is_super_skunk(self) -> bool:
        return self.roll1 == 1 and self.roll2 == 1
            




class Player(BaseModel):
    name: str
    id: str =  Field(default_factory=lambda: str(uuid4()))

    def __hash__(self) -> int:
        return hash(self.id)


class PlayerLockInEvent(BaseModel):
    player: Player


class Round(BaseModel):
    players: Set[Player] = Field(default_factory=set)
    events: List[Union[DiceRoll, PlayerLockInEvent]] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def new(cls) -> Round:
        return Round()

    def add_player(self, player: Player) -> None:
        self.players.add(player)

    def add_roll(self, roll: DiceRoll):
        if self.is_over:
            raise TypeError("Round over.  No more rolls can be added.")
        self.events.append(roll)

    @property
    def rolls(self) -> List[DiceRoll]:
        return [e for e in self.events if isinstance(e, DiceRoll)]

    @property
    def is_over(self) -> bool:
        return any(roll.is_skunk() for roll in self.rolls)

    def add_lockin(self, player: Player):
        if self.is_over:
            raise TypeError("Round over.  Too late to lock in score.")
        
        event = PlayerLockInEvent(player=player)
        self.events.append(event)

    @property
    def scores(self) -> Dict[Player, int]:
        final_scores = {}
        running_score = 0
        for event in self.events:
            if isinstance(event, DiceRoll):
                if event.is_skunk():
                    for player in self.players:
                        if player not in final_scores:
                            final_scores[player] = 0
                    break
                running_score += event.sum()
            elif isinstance(event, PlayerLockInEvent):
                final_scores[event.player] = running_score
            else:
                raise TypeError(f"Event not Handled: {event}")
        else:
            for player in self.players:
                if player not in final_scores:
                    final_scores[player] = running_score

            
        return final_scores
            



                




class Game(BaseModel):
    players: List[Player] = Field(default_factory=list) 
    id: str =  Field(default_factory=lambda: str(uuid4()))
    rolls: List[DiceRoll] = Field(default_factory=list)

    @classmethod
    def new(cls) -> Game:
        return Game()

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def find_players_by_name(self, name: str):
        return [player for player in self.players if player.name == name]

    def get_last_roll(self) -> Optional[DiceRoll]:
        return self.rolls[-1] if len(self.rolls) else None

    def add_dice_roll(self, dice_roll: DiceRoll) -> None:
        self.rolls.append(dice_roll)
        

class Settings(BaseModel):
    games: List[Game] = Field(default_factory=list)
    
    def add_game(self, game: Game) -> None:
        self.games.append(game)
        
    def get_game(self, game_id: str) -> Game:
        games = {game.id: game for game in self.games}
        game = games[game_id]
        return game
        

