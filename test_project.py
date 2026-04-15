import pytest
from project import create_game, setup_game, play_poker
from game import Game

def test_create_game():
    game = create_game()
    assert isinstance(game, Game)

def test_setup_game(monkeypatch):

    game = Game()

    inputs = iter([
        "",          # press enter to continue
        "TestPlayer"          # player name
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    monkeypatch.setattr("game.sleep", lambda x: None)

    setup_game(game)

    assert game._round == 0
    assert game._players[0].name == "TestPlayer"
    assert game._players[1].name == "Computer"
    assert game._players[0].chips and game._players[1].chips == 100
    assert game._deck is not None
    assert game._table is not None

def test_play_game(monkeypatch):
    game = Game()

    # All inputs in one iterator:
    # 1-2 for setup, then 2 for rounds
    inputs = iter([
        "",            # setup: press enter
        "TestPlayer",  # setup: player name
        "",            # _pay_blinds: press enter
        "",            # see hands: press enter
        "",            # _flop: press enter
        "check",       # round 1 player action
        "",            # _turn: press enter
        "fold",        # round 2 player action
        ""             # passes text showing winner
        
        # ends test was fake exit
    ])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))

    # Remove sleep delays
    monkeypatch.setattr("game.sleep", lambda x: None)

    # Setup game
    setup_game(game)

    # Fix computer choices
    monkeypatch.setattr("random.choice", lambda options: options[0])

    # Control rounds: stop after 2
    rounds = iter([True, False])
    monkeypatch.setattr(game, "_check_game_winner", lambda: next(rounds))

    # Run game
    play_poker(game)

    # Assertions
    # ensure game round is going up per round
    assert game._round >= 1
    # ensure player names are the same
    assert game._players[0].name == "TestPlayer"
    assert game._players[1].name == "Computer"
    # ensure cleanup happened
    assert game._table.cards == []
    assert game._table.pot == 0
    for player in game._players:
        assert player.hand == []
