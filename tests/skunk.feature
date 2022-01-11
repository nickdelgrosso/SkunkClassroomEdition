Feature: Skunk Game

    Scenario: Host starts a new game
        Given two new games have been created
        When the player goes to the game list page
        Then players will see the two games

    Scenario: Player registers themselves to a new game
        Given one new game has been started
        When Nick submits his name to the game
        Then Nick will be in the game player list 

    Scenario: Dice Rolling
        Given a game has just been started
        And no dice rolls are visible on the game details
        When the dice are rolled
        Then the last roll will be visible on the game details

    # Scenario: Score Checking
    #     Given a game has been started
    #     When the game status is checked
    #     Then all the player scores for each round will be visible
    #     And the player total scores will be visible
        