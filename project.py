from game import Game

# Poker Project
# Lee Faria
# Github: NeutralAlign
# edX: lee_972
# London, UK
# Date: 15/04/2026

def main():
    game = create_game()
    setup_game(game)
    play_poker(game)

def create_game():
    return Game()

def setup_game(game: Game):
    game.setup()

def play_poker(game: Game):
    game.play()

if __name__ == "__main__":
    main()
