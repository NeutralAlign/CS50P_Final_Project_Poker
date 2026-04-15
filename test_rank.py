import pytest
from cards import Card
from rank import evaluate_hand, compare_hands, card_ranking


def test_high_card():
    hand = [
        Card("A", "♠️"),
        Card("7", "♦️"),
        Card("4", "♣️"),
        Card("2", "♥️"),
        Card("9", "♠️")
    ]

    rank, _ = evaluate_hand(hand)
    assert rank == 1


def test_pair():
    hand = [
        Card("A", "♠️"),
        Card("A", "♦️"),
        Card("4", "♣️"),
        Card("2", "♥️"),
        Card("9", "♠️")
    ]

    rank, _ = evaluate_hand(hand)
    assert rank == 2


def test_compare_hands():
    hand1 = [
        Card("A", "♠️"),
        Card("A", "♦️"),
        Card("4", "♣️"),
        Card("2", "♥️"),
        Card("9", "♠️")
    ]

    hand2 = [
        Card("K", "♠️"),
        Card("K", "♦️"),
        Card("4", "♣️"),
        Card("2", "♥️"),
        Card("9", "♠️")
    ]

    winner, _ = compare_hands(hand1, hand2)

    assert winner == 1


def test_card_ranking():
    assert card_ranking(10) == "royal flush"
    assert card_ranking(5) == "straight"
