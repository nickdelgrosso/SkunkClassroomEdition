from __future__ import annotations

import random
from dataclasses import dataclass, field, asdict
from typing import Optional, List
from uuid import uuid4, UUID
import json

from fastapi import FastAPI
import jinja2

@dataclass
class Player:
    name: str
    id: str = field(default_factory=lambda: str(uuid4()))



@dataclass(frozen=True)
class Game:
    players: List[Player] = field(default_factory=list) 
    id: str = field(default_factory=lambda: str(uuid4()))

    @classmethod
    def new(cls) -> Game:
        return Game()

    def add_player(self, player: Player) -> None:
        self.players.append(player)


@dataclass()
class Settings:
    games: List[Game] = field(default_factory=list)
    
    def add_game(self, game: Game) -> None:
        self.games.append(game)
        
    def get_game(self, game_id: str) -> Game:
        games = {game.id: game for game in self.games}
        game = games[game_id]
        return game
        

settings = Settings()


app = FastAPI()

@app.get("/register-new-game")
def start_new_game():
    new_game = Game.new()
    settings.add_game(new_game)
    return {
        "success": True,
        "gameId": new_game.id,
    }

@app.get("/games")
def homepage():
    return {
        'games': {game.id: {'players': [{'id': player.id, 'name': player.name} for player in game.players]} for game in settings.games}
    }


@app.get("/register")
def regiser_player(game_id: str, player_name: str):
    try:
        game = settings.get_game(game_id)
    except KeyError:
        return {
            "success": False,
            "msg": f"Game ID Not Found: {game_id}"
        }
    player = Player(name=player_name)
    game.add_player(player)
    return {
        "success": True,
        "playerId": player.id,
        "gameId": game.id
    }
