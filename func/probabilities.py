"""Probability and simulation functions."""

import random
from copy import deepcopy

from func.moxfield import DeckList
from func.cardpool import CardPool


def simulate_probability(iterations: int, deck_json: dict,
                         account_generic=True, override_mt=None) -> dict:
    """
    Simulates the probability of hitting your mana target on curve.
    :param iterations: Number of iterations for the simulation. A good starting point is 1k.
    :param deck_json: The JSON file of the deck.
    :param account_generic: True (default) if you're looking to hit your commander's manas. False if colours are enough.
    :param override_mt: A custom ManaTarget object if you want to override the commander-based mana target.
    :return: Dict of commander_names, probability, mana_target (ManaTarget).
    """
    decklist = DeckList(deck_json=deck_json)
    start_deck = CardPool(decklist)
    start_hand = CardPool(DeckList(deck_json={}))
    successes = 0
    if override_mt:
        mana_target = override_mt
    else:
        mana_target = start_deck.target
    draws = mana_target.total_mana() + 7

    commander_names = []
    for commander_card in decklist.commanders:
        commander_names.append(commander_card.name)

    for _ in range(0, iterations):
        deck = deepcopy(start_deck)
        hand = deepcopy(start_hand)
        for _ in range(0, draws):
            draw = random.choice(deck.cards)
            deck.remove_card(draw)
            hand.add_card(draw)

        if hand.success(mana_target, account_generic):
            successes += 1

    return {'names': commander_names, 'probability': (successes / iterations), 'mana_target': mana_target}


def simulate_turns(iterations: int, deck_json: dict,
                   account_generic=True, override_mt=None) -> dict:
    """
    Simulates the number of turns it takes to hit your mana target.
    :param iterations: Number of iterations for the simulation. A good starting point is 1k.
    :param deck_json: The JSON file of the deck.
    :param account_generic: True (default) if you're looking to hit your commander's manas. False if colours are enough.
    :param override_mt: A custom ManaTarget object if you want to override the commander-based mana target.
    :return: Dict of commander_names (list), turns (float), mana_target (ManaTarget).
    """
    decklist = DeckList(deck_json=deck_json)
    start_deck = CardPool(decklist)
    start_hand = CardPool(DeckList(deck_json={}))
    turn_counts = []
    if override_mt:
        mana_target = override_mt
    else:
        mana_target = start_deck.target

    commander_names = []
    for commander_card in decklist.commanders:
        commander_names.append(commander_card.name)

    for _ in range(0, iterations):
        deck = deepcopy(start_deck)
        hand = deepcopy(start_hand)
        draw_count = 0
        while not hand.success(mana_target, account_generic):
            draw = random.choice(deck.cards)
            deck.remove_card(draw)
            hand.add_card(draw)
            draw_count += 1
        turn_counts.append(draw_count - 7)

    return {'names': commander_names, 'turns': (sum(turn_counts) / iterations), 'mana_target': mana_target}