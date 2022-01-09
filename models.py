from __future__ import annotations


from typing import Optional, List
from uuid import uuid4, UUID
from pydantic import BaseModel, Field




class Player(BaseModel):
    name: str
    id: str =  Field(default_factory=lambda: str(uuid4()))


class Game(BaseModel):
    players: List[Player] = Field(default_factory=list) 
    id: str =  Field(default_factory=lambda: str(uuid4()))

    @classmethod
    def new(cls) -> Game:
        return Game()

    def add_player(self, player: Player) -> None:
        self.players.append(player)

    def find_players_by_name(self, name: str):
        return [player for player in self.players if player.name == name]



class Settings(BaseModel):
    games: List[Game] = Field(default_factory=list)
    
    def add_game(self, game: Game) -> None:
        self.games.append(game)
        
    def get_game(self, game_id: str) -> Game:
        games = {game.id: game for game in self.games}
        game = games[game_id]
        return game
        

