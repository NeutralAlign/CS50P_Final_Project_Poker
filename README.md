# Poker Project
#### Video Demo:  <https://youtu.be/fKLQFWOBxYk>
#### Description:

##### What is the project?

This project is a player versus computer Poker game that I made for the final project in CS50P. It follows the standard Texas Hold'em rules where each player gets 2 cards and the table gets 5 cards. The game continues until a player runs out of chips.

##### Running the project

Simply use 'python project.py' to run the project when importing the source code. project.py automatically has the required functions to run Poker. If you intend to change the default code, please review the file breakdown section for more details.

##### Code Design

I decided to create Poker using an object-oriented design because it seemed fitting with many objects that could be represented as a class (such as cards, deck, players, table). This also was a good time to try creating the game itself as an object, which is great for only storing game logic rather than having it all in the main file which could be confusing.

This allows us to simply create a new instance of the game class which is much more efficient and readable and run like so:

1. game = create_game()
2. setup_game(game)
3. play_poker(game)

...where the main logic is abstracted away by class methods.

##### File Breakdown
In this project, we have 7 files each with their own responsibilities. Each are listed in more depth below.

###### project.py

This is the file which runs the game of Poker. It is split into 3 main functions:

* create_game() creates a game object from the game class and returns it to a variable.

* setup_game(game) takes a game object and initialises the players, deck and table. (currently only Player vs Computer)

* play_poker(game) takes a game object and runs through the poker game loop via the game class.

I originally had this as just a single function you called in main, but due to the requirements of the project I split these into 3 functions here.

###### game.py

This is the file which has the game and setup logic for Poker in the game class. It is split into:

* The setup which creates player, computer, table and deck instances (and the round counter).

* The main gameplay loop:

1. If a player runs out of chips, end the game, else, play a round of Poker.
2. Shuffle the deck.
3. Players pay blinds.
4. Players are dealt cards and cards are revealed (for player only).
5. There is a flop, turn and river, the latter two allowing the player and computer to take actions (check, bet, fold etc).
6. Winner is chosen.
7. Chips are awarded.
8. Repeat.

###### rank.py

This is the file which has helper functions to evaluate player hands. It is split into:

* evaluate_hand(hand) which takes in a player hand and returns a tuple in the format of (rank, kickers) for comparing hands. This works by using other helper functions, each detecting a type of hand (pair, two pair, flush etc) from highest rank (royal flush) to lowest (high card).

* compare_hands(hand_1, hand_2) which takes in two hands and returns the winner (1 for player, 2 for computer or 0 for tie). This works by comparing the hand ranking, and in a tie, the tiebreaker cards (kickers).

* card_ranking(rank_number) which simply takes a rank number (1-10) and outputs a string with the rank name, e.g input of 1 will return "high card".

* group_by_suit(hand) which takes a player hand and creates a dictionary which contains suits as keys and the card numbers as values. Used in some hand ranking functions (like flush).

* pair(values) returns the pair and kicker values of a player hand (if it exists).

* two_pair(values) returns the two pair and kicker values of a player hand (if it exists).

* three_of_a_kind(values) returns the three of a kind and kicker values of a player hand (if it exists).

* straight(values) returns the straight values of a player hand (if it exists).

* flush(hand) returns the flush values of a player hand (if it exists).

* four_of_a_kind(values) returns the four of a kind and kicker values of a player hand (if it exists).

* full_house(values) returns the full house (pair and three of a kind) values of a player hand (if it exists).

* straight_flush(hand) returns the straight flush values of a player hand (if it exists).

* royal_flush(hand) returns the royal flush values of a player hand (if it exists).

###### player.py

This file contains the player class which contains:

* Name, hand and chip count attributes and methods to manipulate (adding or removing chips / cards for example).
* Standard poker actions that each player can take as methods (bet, check, fold etc)

###### cards.py

This file contains multiple classes, including:

* Card class which represents playing cards by their suit and rank.
* Table class which holds a list of playing cards and a central pot for chips.
* Deck class which is used to create a full deck of playing cards (with methods such as dealing to players, shuffling etc)

###### test_project.py

This file tests the following:

* create_game() returns a game object.
* setup_game() sets the round, player, deck and table attributes and assigns them their objects (where applicable) using monkeypatch to simulate a user.
* Simulates a round of poker using play_poker() and monkeypatch with predefined actions.

All test cases passed with pytest.

###### test_rank.py

This file tests the following:

* evaluate_hand function returns 1 when the player hand contains only a high card.
* evaluate_hand function returns 2 when the player hand contains a pair.
* compare_hands function accurately can tell apart which player has the better pair.
* card_ranking function gives the correct hand ranking for a ranking number.

All test cases passed with pytest.

##### Future Ideas

Here are some ideas I had which could be added in the future to improve upon it:

* Dynamic number of players and / or computer to play with (to a limit).
* Improved computer AI should be researched and add.
* Dynamic small and big blind options.
* GUI would improve the user experience.
* Multiple methods should be more dynamic for multiple players and should be a focus next time.
* Add a new attribute to record player actions to the player class.
* More indepth testing for edge cases should be done (double ALL-IN for example).
* Remove redundant functions in project.py.
* Clean up and / or refactoring can be done.
* Possibly some redundant methods in classes that could be removed.

##### End

Thank you to the CS50 team for another wonderful course and the opportunity to learn and grow further with the final project, it was a lot of fun! This was CS50P!
