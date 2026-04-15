from cards import Table, Deck
from player import Player
from time import sleep
from rank import compare_hands, card_ranking
import random

class Game:

    def _add_players(self):
        # list used to sort player and computer object
        self._players = []

        while True:
            name = input(f"Enter name for Player: ").strip()
            if name:
                break

        self._players.append(Player(name))
        self._players.append(Player("Computer"))

    def _create_table(self):
        # creates and stores the table for this game
        self._table = Table()

    def _create_deck(self):
        # creates and stores the deck for this game
        self._deck = Deck()

    def setup(self):
        # used to initalize the game
        print()
        print("### POKER ###")
        sleep(0.5)
        input("Press Enter to continue...")
        print()
        self._add_players()
        print()
        self._create_table()
        self._create_deck()
        self._round = 0

    def _shuffle_deck(self):
        # shuffles the deck
        self._deck.shuffle()

    def _deal_players(self):
        # deals the players 2 cards each
        for player in self._players:
            self._deck.deal_player(player)

    def _reveal_hands(self):
        for player in self._players:
            if player.name == "Computer":
                print(f"Computer's Hand: ?")
            else:
                print(player.status())
        input()

    def _flop(self):
        # flop (3 cards on table)
        print("### FLOP ###")
        self._deck.deal_table(self._table, n=3)
        print(self._table)
        input()

    def _turn(self):
        # turn (1 more card to table)
        print("### TURN ###")
        self._deck.deal_table(self._table)
        print(self._table)
        input()

    def _river(self):
        print("### RIVER ###")
        # river (last card added to table)
        self._deck.deal_table(self._table)
        print(self._table)
        input()

    def _check_game_winner(self):
        # assesses if a new round is needed
        winner = ""
        loser = ""

        if self._players[0].chips == 0:
            winner = self._players[1].name
            loser = self._players[0].name
        elif self._players[1].chips == 0:
            winner = self._players[0].name
            loser = self._players[1].name

        if winner:
            print(f"{loser} has ran out of chips, {winner} has won!")
            print()

            if input(f"Play again? (Y/N) ").lower() == "y":
                print()
                self._round = 0

                for player in self._players:
                    player.chips = 100

                return True

            else:
                return False
        return True

    def _cleanup(self):
        # reset all player hands and last action
        for player in self._players:
            player.reset_hand()

        # reset table
        self._table.reset_table()
        self._table.reset_pot()

    def _play_round(self):
        winner = None
        self._round += 1

        print(f"### ROUND {self._round} ###")
        self._shuffle_deck()
        self._pay_blinds(1, 5)
        self._deal_players()
        self._reveal_hands()
        self._flop()

        winner = self._player_action()

        if winner:
            self._pay_round_winner(winner)
            return

        self._turn()

        winner = self._player_action()

        if winner:
            self._pay_round_winner(winner)
            return

        self._river()
        self._pay_round_winner(self._round_winner())

    def play(self):
        # important change: implemented loop rather than recursively calling play to avoid stack overflow
        while True:
            if not self._check_game_winner():
                break
            self._play_round()
            self._cleanup()

    def _pay_blinds(self, small_blind, big_blind):
        # allows rotation on player and computer
        small_index = self._round % 2
        big_index = 1 - small_index

        # each player pays a blind
        small_blind_paid = self._players[small_index].remove_chips(small_blind)
        big_blind_paid = self._players[big_index].remove_chips(big_blind)

        if small_blind_paid == small_blind:
            print(f"{self._players[small_index].name} paid {small_blind_paid} for the small blind.")
        else:
            print(f"{self._players[small_index].name} paid {small_blind_paid} for the small blind and is ALL-IN!")
        self._table.add_to_pot(small_blind_paid)

        if big_blind_paid == big_blind:
            print(f"{self._players[big_index].name} has paid {big_blind_paid} for the big blind.")
        else:
            print(f"{self._players[big_index].name} has paid {big_blind_paid} for the big blind and is ALL-IN!")
        self._table.add_to_pot(big_blind_paid)

        input()

    def _player_action(self):
        player = self._players[0]
        computer = self._players[1]

        total_bet = 0
        player_action = None

        while True:
            print(f"Pot: {self._table.pot}\nYour Chips: {player.chips}\n")

            if player.chips == 0 and computer.chips == 0:
                print(f"Both players are ALL-IN.\n")
                return

            if player.chips == 0:
                print(f"{player.name} is ALL-IN.\n")

                if total_bet == 0:
                    computer.check()
                else:
                    computer.call(total_bet)
                    self._table.add_to_pot(total_bet)
                return


            # player action
            if total_bet == 0:
                while player_action not in ["check", "bet", "fold"]:
                    player_action = input("Actions: Check, Bet, Fold\nAction: ").lower().strip()
                    print()

                if player_action == "check":
                    player.check()

                elif player_action == "bet":
                    total_bet = player.bet()
                    self._table.add_to_pot(total_bet)

                elif player_action == "fold":
                    player.fold()
                    return computer

            else:

                while player_action not in ["call", "raise", "fold"]:
                    player_action = input("Actions: Call, Raise, Fold\nAction: ").lower().strip()
                    print()

                if player_action == "call":
                    player.call(total_bet)
                    self._table.add_to_pot(total_bet)
                    return

                elif player_action == "raise":
                    new_total_bet = player.raise_bet(total_bet)
                    total_bet = new_total_bet
                    self._table.add_to_pot(new_total_bet)

                elif player_action == "fold":
                    player.fold()
                    return computer

            player_action = None

            # computer actions
            if computer.chips == 0:
                print(f"{computer.name} is ALL-IN.\n")
                return

            if total_bet == 0:
                choice = random.choice(("check", "bet"))

                if choice == "check":
                    computer.check()
                    return

                if choice == "bet":
                    bet_amount = random.randint(1, computer.chips)
                    total_bet = computer.bet(bet_amount)
                    self._table.add_to_pot(total_bet)

            else:

                if player.chips == 0:
                    choice = random.choice(("call", "fold"))
                else:
                    choice = random.choice(("call", "raise", "fold"))

                if choice == "call":
                    computer.call(total_bet)
                    self._table.add_to_pot(total_bet)
                    return

                if choice == "raise":
                    raise_amount = random.randint(1, computer.chips)
                    new_total_bet = computer.raise_bet(total_bet, raise_amount)
                    total_bet = new_total_bet
                    self._table.add_to_pot(new_total_bet)

                if choice == "fold":
                    computer.fold()
                    return player


    def _round_winner(self):
        print("### SHOWDOWN ###")
        player = self._players[0]
        computer = self._players[1]

        print(f"{player.name}'s hand revealed: {player.fmt_card()}")
        print(f"Computer's hand revealed: {computer.fmt_card()}")
        input()

        player_hand = player.hand + self._table.cards
        computer_hand = computer.hand + self._table.cards

        result, rank = compare_hands(player_hand, computer_hand)

        if result == 1:
            print(f"{player} won with a {card_ranking(rank)}!")
            return player
        elif result == 2:
            print(f"{computer} won with a {card_ranking(rank)}!")
            return computer
        else:
            print("Both players tied!")
            return None  # tie


    def _pay_round_winner(self, winner):
        if winner:
            chips = self._table.pot
            print(f"{winner} won and got {chips} chips!")
            winner.add_chips(chips)
            input()
        else:
            chips = self._table.pot // 2
            print(f"Both players got {chips} chips!")
            input()
            for player in self._players:
                player.add_chips(chips)








