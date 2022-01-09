from __future__ import annotations


import random
from typing import Optional, List, Tuple
from uuid import uuid4
from pydantic import BaseModel, Field, validator



class DiceRoll(BaseModel):
    roll1: int
    roll2: int

    @validator('roll1', 'roll2')
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




class Player(BaseModel):
    name: str
    id: str =  Field(default_factory=lambda: str(uuid4()))


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
        

