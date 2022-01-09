import pytest
from pytest_bdd import given, when, then, scenarios
from pytest_bdd.parsers import parse
from fastapi.testclient import TestClient
from starlette.responses import Response

from routes import GameListResponse, Game
from main import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)



scenarios(".")



@given("two new games have been created")
def stepdef(client):
    client.get("/register-new-game")
    client.get("/register-new-game")
    


@when("the player goes to the game list page", target_fixture="response")
def stepdef(client):
    response = client.get("/games")
    return response    


@then("players will see the two games")
def stepdef(response: Response):
    data = response.json()
    assert len(data['games']) == 2, data


@given("one new game has been started", target_fixture="game_id")
def stepdef(client):
    data = client.get("/register-new-game").json()
    return data['gameId']


@when(
    parse("{player_name} submits his name to the game"), 
    target_fixture="response"
)
def stepdef(client: TestClient, game_id: str, player_name: str):
    response = client.get(f"/register?game_id={game_id}&player_name={player_name}")
    return response
    

@then("Nick will be in the game player list")
def stepdef(client: TestClient, response: Response):
    data = response.json()
    game_data = client.get("/games").json()
    games = GameListResponse.parse_obj(game_data)    
    game = Game.parse_obj(games.get_game(data['gameId']))
    players = game.find_players_by_name('Nick')
    assert len(players) == 1, players
    
    
