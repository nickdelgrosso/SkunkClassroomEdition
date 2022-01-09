from __future__ import annotations
from typing import List, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID

from pydantic.fields import Field
from requests.models import HTTPError

from models import Game, Settings, Player, DiceRoll


settings = Settings()


app = FastAPI()

class GameRegistration(BaseModel):
    gameId: str


@app.get("/register-new-game", response_model=GameRegistration)
def start_new_game():
    new_game = Game.new()
    settings.add_game(new_game)
    return GameRegistration(success=True, gameId=new_game.id)



class GameListResponse(BaseModel):
    games: List[Game]

    def get_game(self, id: UUID) -> Game:
        games = {game.id: game for game in self.games}
        game = games[id]
        return game
        

@app.get("/games", response_model=GameListResponse)
def list_games() -> GameListResponse:
    return GameListResponse(games=settings.games)


class PlayerRegistrationResponse(BaseModel):
    gameId: str
    player: Player
    

@app.get("/register", response_model=PlayerRegistrationResponse)
def register_player(game_id: str, player_name: str):
    try:
        game = settings.get_game(game_id)
    except KeyError:
        raise HTTPError(status_code=404, detail=f"Game ID Not Found: {game_id}")

    player = Player(name=player_name)
    game.add_player(player)
    return PlayerRegistrationResponse(player=player, gameId=game.id)


class GameDetailsResponse(BaseModel):
    game: Game
    last_roll: Optional[DiceRoll]

@app.get("/game", response_model=GameDetailsResponse)
def show_game_details(id: str):
    try:
        game = settings.get_game(id)
    except KeyError:
        raise HTTPError(status_code=404, detail=f"Game ID Not Found: {id}")

    return GameDetailsResponse(game=game, last_roll=game.get_last_roll())


class RollDiceResponse(BaseModel):
    roll: DiceRoll

@app.get("/roll-dice", response_model=RollDiceResponse)
def roll_dice(game_id: str):
    try:
        game = settings.get_game(game_id)
    except KeyError:
        raise HTTPError(status_code=404, detail=f"Game ID Not Found: {game_id}")

    dice_roll = DiceRoll.new()
    game.add_dice_roll(dice_roll)
    return RollDiceResponse(roll=dice_roll)