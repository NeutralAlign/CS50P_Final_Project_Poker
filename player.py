class Player:
    def __init__(self, name: str):
        self._name = name
        self._hand = []
        self._chips = 100

    def __str__(self):
        return f"{self._name}"

    def __repr__(self):
        return f"{self._name}"

    def fmt_card(self):
        return f"{"  ".join(str(card) for card in self._hand)}"

    @property
    def name(self) -> str:
        return self._name

    @property
    def hand(self) -> list:
        return self._hand

    @property
    def chips(self) -> int:
        return self._chips

    @chips.setter
    def chips(self, n: int) -> None:
        self._chips = n

    def status(self):
        return f"{self._name}'s Hand: {"  ".join(str(card) for card in self._hand)}"

    def add_chips(self, n: int) -> None:
        self._chips += n

    def remove_chips(self, n: int):
        if self._chips - n < 0:
            chips_left = self._chips
            self._chips = 0
            return chips_left
        else:
            self._chips -= n
            return n

    def update_hand(self, card) -> None:
        self._hand.append(card)

    def reset_hand(self) -> None:
        self._hand = []

    def check(self):
        print(f"{self._name} checks.\n")

    def bet(self, value=None):
        if value:
            bet = value
            if bet == self._chips:
                print(f"{self._name} {bet} chips is ALL-IN!\n")
            else:
                print(f"{self._name} bets {bet} chips.\n")
            self.remove_chips(bet)
            return bet

        bet = 0
        while True:
            while True:
                try:
                    bet = int(input("Bet Amount: "))
                    if bet <= 0:
                        raise ValueError
                    break
                except(ValueError):
                    print("Please enter a valid integer.")

            if bet >= self._chips:
                bet = self._chips
            if input(f"Confirm bet: {bet} (Y/N) ").lower() == "y":
                print()
                if bet == self._chips:
                    print(f"{self._name} {bet} chips is ALL-IN!\n")
                else:
                    print(f"{self._name} bets {bet} chips.\n")

                self.remove_chips(bet)
                return bet
            print()

    def raise_bet(self, total_bet, raise_amount=None):
        # Computer raise
        if raise_amount is not None:

            total_amount = total_bet + raise_amount

            if total_amount >= self._chips:
                total_amount = self._chips
                raise_amount = total_amount - total_bet
                print(f"{self._name} raises by {raise_amount} chips and is ALL-IN!\n")
            else:
                print(f"{self._name} raises by {raise_amount} chips.\n")

            self.remove_chips(total_amount)
            return raise_amount

        # Player raise
        while True:
            while True:
                try:
                    raise_amount = int(input("Amount to raise: "))
                    if raise_amount <= 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Please enter a valid integer.")

            total_amount = total_bet + raise_amount

            if total_amount >= self._chips:
                total_amount = self._chips
                raise_amount = total_amount - total_bet

            if input(f"Confirm raise: {raise_amount} (Y/N) ").lower() == "y":

                if total_amount == self._chips:
                    print(f"{self._name} raises by {raise_amount} chips and is ALL-IN!\n")
                else:
                    print(f"{self._name} raises by {raise_amount} chips.\n")

                self.remove_chips(total_amount)
                return raise_amount

    def call(self, call_amount):
        if call_amount >= self._chips:
            call_amount = self._chips

        if call_amount == self._chips:
            print(f"{self._name} calls with {call_amount} chips is ALL-IN!\n")
        else:
            print(f"{self._name} calls with {call_amount} chips.\n")

        self.remove_chips(call_amount)

    def fold(self):
        print(f"{self._name} folds.\n")


