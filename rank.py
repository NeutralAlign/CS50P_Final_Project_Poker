from collections import Counter
# helper functions to rank hands (winning hand logic)

def pair(values):
    value_counts = Counter(values)

    pair_value = None

    for value in value_counts:
        if value_counts[value] == 2:
            pair_value = value
            break

        if pair_value is None:
            return None

    # get every card value in values that are not the pair value (kickers for tie breakers)
    kickers = [value for value in values if value != pair_value]
    # only keep the top 3 kickers for a pair (max hand is 5, a pair takes two options away)
    kickers = sorted(kickers[:3], reverse = True)

    return pair_value, kickers


def two_pair(values):
    value_counts = Counter(values)

    # get all values that appear exactly twice
    pairs = [value for value, count in value_counts.items() if count == 2]

    # need at least 2 pairs
    if len(pairs) < 2:
        return None

    # take the top two pairs
    top_pairs = sorted(pairs, reverse=True)[:2]
    first_pair, second_pair = top_pairs

    # remove all cards from both pairs to find kicker
    kickers = [v for v in values if v != first_pair and v != second_pair]
    kicker = max(kickers) if kickers else None

    return first_pair, second_pair, kicker

def three_of_a_kind(values):
    value_counts = Counter(values)

    three_kind_value = None

    for value in value_counts:
        if value_counts[value] == 3:
            three_kind_value = value
            break

    if not three_kind_value:
        return None

    kickers = [v for v in values if v != three_kind_value]
    kickers = sorted(kickers, reverse = True)[:2]

    return three_kind_value, kickers

def straight(values):
    values = sorted(set(values), reverse = True)

    straight_values = None

    # sliding window for 5 consecutive numbers
    # e.g if 7 numbers, we slide the window 7 - 4 -> (3) times checking for a straight
    for i in range(len(values) - 4):
        highest = values[i]
        lowest = values[i + 4]

        # checks if the window has a straight (5 consecutive numbers)
        if highest - lowest == 4:
            straight_values = values[i: i + 5]
            break

    # check ace exception
    if {14,2,3,4,5}.issubset(values):
        straight_values = [1,2,3,4,5]

    if not straight_values:
        return None

    return straight_values

def flush(hand):
    suit_groups = group_by_suit(hand)

    for values in suit_groups.values():
        if len(values) >= 5:
            return sorted(values, reverse = True)[:5]

    return None


def four_of_a_kind(values):
    value_counts = Counter(values)

    four_kind_value = None

    for value in value_counts:
        if value_counts[value] == 4:
            four_kind_value = value
            break

    if not four_kind_value:
        return None

    kickers = [v for v in values if v != four_kind_value]
    kicker = sorted(kickers, reverse = True)[:1]

    return four_kind_value, kicker

def full_house(values):
    value_counts = Counter(values)

    # key is the number, value is the count
    three_kind_values = [key for key, value in value_counts.items() if value >= 3]

    if not three_kind_values:
        return None

    three_kind_value = max(three_kind_values)

    pair_values = [key for key, value in value_counts.items() if value >= 2 and key != three_kind_value]

    if not pair_values:
        return None

    pair_value = max(pair_values)

    return three_kind_value, pair_value

def straight_flush(hand):
    suit_groups = group_by_suit(hand)

    for values in suit_groups.values():
        if len(values) >= 5:
            straight_values = straight(values)
            if straight_values:
                return sorted(straight_values, reverse = True)
    return None


def royal_flush(hand):
    suit_groups = group_by_suit(hand)

    royal_cards = {14, 13, 12, 11, 10}

    for values in suit_groups.values():
        if royal_cards.issubset(values):
            return sorted(royal_cards, reverse = True)
    return None


def evaluate_hand(hand):
    # get a sorted list of the values (2-14) in the player hand + table cards
    values = sorted([card.value for card in hand], reverse = True)

    royal_flush_result = royal_flush(hand)
    if royal_flush_result:
        return (10, royal_flush_result)

    straight_flush_result = straight_flush(hand)
    if straight_flush_result:
        return (9, straight_flush_result)

    full_house_result = full_house(values)
    if full_house_result:
        three_kind_value, pair_value = full_house_result
        return (8, [three_kind_value, pair_value])

    four_of_a_kind_result = four_of_a_kind(values)
    if four_of_a_kind_result:
        four_kind_value, kicker = four_of_a_kind_result
        return (7, [four_kind_value, kicker])

    flush_result = flush(hand)
    if flush_result:
        return (6, flush_result)

    straight_result = straight(values)
    if straight_result:
        return (5, straight_result)

    three_of_a_kind_result = three_of_a_kind(values)
    if three_of_a_kind_result:
        three_of_a_kind_value, kickers = three_of_a_kind_result
        return (4, [three_of_a_kind_value] + kickers)

    two_pair_result = two_pair(values)
    if two_pair_result:
        first_pair, second_pair, kicker = two_pair_result
        return (3, [first_pair, second_pair, kicker])

    pair_result = pair(values)
    if pair_result:
        pair_value, kickers = pair_result
        return (2, [pair_value] + kickers)

    return (1, values[:5])

def compare_hands(hand_1, hand_2):
    # this will then take that data from evaluate hand, and see who wins
    rank_1, tiebreakers_1 = evaluate_hand(hand_1)
    rank_2, tiebreakers_2 = evaluate_hand(hand_2)

    # compare the hand ranks first
    if rank_1 > rank_2:
        return 1, rank_1  # hand 1 wins
    elif rank_2 > rank_1:
        return 2, rank_2  # hand 2 wins

    # if same rank, compare tie-breakers
    # zip creates pairs of tuples used to compare each element that pairs up with each other
    for v1, v2 in zip(tiebreakers_1, tiebreakers_2):
        if v1 > v2:
            return 1, rank_1
        elif v2 > v1:
            return 2, rank_2

    # if all tie-breakers equal, it's a tie
    return 0, None

def card_ranking(rank_number):
    # given a card ranking number, return the name of the ranking
    ranks = {
        1: "high card",
        2: "pair",
        3: "two pair",
        4: "three of a kind",
        5: "straight",
        6: "flush",
        7: "four of a kind",
        8: "full house",
        9: "straight flush",
        10: "royal flush"
    }

    if rank_number in ranks:
        return ranks[rank_number]
    return None

def group_by_suit(hand):
    groups = {}

    for card in hand:
        if card.suit not in groups:
            groups[card.suit] = []

        groups[card.suit].append(card.value)

    return groups

