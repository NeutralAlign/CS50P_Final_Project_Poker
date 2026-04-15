import random
from player import Player

RANK_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

class Card:
    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    def __str__(self):
        # single representation of a Card object
        return f"{self._rank}{self._suit}"

    def __repr__(self):
        # returns representation of Card objects from list
        return f"{self._rank}{self._suit}"

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def value(self):
        return RANK_VALUES[self.rank]

class Table:

    def __init__(self):
        self._cards = []
        self._pot = 0

    def __str__(self):
        if self._cards:
            #joins the card strings with spaces
            return f"Table: {"  ".join(str(card) for card in self._cards)}"
        else:
            return "No cards on this table"

    @property
    def cards(self):
        return self._cards

    @property
    def pot(self):
        return self._pot

    def reset_pot(self):
        self._pot = 0

    def add_to_pot(self, n):
        self._pot += n

    def reset_table(self):
        # removes cards on the table
        self._cards = []

    def place_card(self, card):
        self._cards.append(card)

class Deck:
    def __init__(self):
        self._deck = self._create_deck()

    @property
    def deck(self):
        # returns the list of cards from the deck
        return self._deck

    def _create_deck(self):
        # creates a new deck of cards
        deck = []
        for suit in ["♣️", "♠️", "♥️", "♦️"]:
            for rank in range(1, 14):
                if rank > 10 or rank == 1:
                    match rank:
                        case 1:
                            deck.append(Card("A", f"{suit}"))
                        case 11:
                            deck.append(Card("J", f"{suit}"))
                        case 12:
                            deck.append(Card("Q", f"{suit}"))
                        case 13:
                            deck.append(Card("K", f"{suit}"))
                else:
                    deck.append(Card(f"{rank}", f"{suit}"))
        return deck

    def shuffle(self):
        # shuffles the deck of cards (and makes a new deck if missing cards)
        if len(self._deck) != 52:
            self._deck = self._create_deck()
        random.shuffle(self._deck)

    def deal_player(self, player: Player) -> None:
        # selects a player and deals cards to them
        if player.hand:
            player.reset_hand()
        for _ in range(2):
            player.update_hand(self._deck.pop())

    def deal_table(self, table: Table, n=1):
        # deal n cards
        for _ in range(n):
            table.place_card(self._deck.pop())

    def check_deck(self) -> int:
        # returns the number of cards in the deck
        return len(self._deck)
