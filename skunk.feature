Feature: Skunk Game

    Scenario: Host starts a new game
        Given two new games have been created
        When the player goes to the game list page
        Then players will see the two games

    Scenario: Player registers themselves to a new game
        Given one new game has been started
        When Nick submits his name to the game
        Then Nick will be in the game player list 

    