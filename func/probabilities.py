"""Probability and simulation functions."""

import asyncio
import random

from func.moxfield import DeckList
from func.cardpool import success


async def simulate_probability(iterations: int, deck_json: dict,
                               account_generic: bool = True, override_mt: list = None) -> dict:
    """
    Simulates the probability of hitting your mana target on curve.
    :param iterations: Number of iterations for the simulation. A good starting point is 1k.
    :param deck_json: The JSON file of the deck.
    :param account_generic: True (default) if you're looking to hit your commander's manas. False if colours are enough.
    :param override_mt: A custom ManaTarget object if you want to override the commander-based mana target.
    :return: Dict of commander_names, probability, mana_target (ManaTarget).
    """
    decklist = DeckList(deck_json=deck_json)

    if override_mt:
        mana_target = override_mt
    else:
        mana_target = decklist.get_mana_target()

    commander_names = []
    for commander_card in decklist.commanders:
        commander_names.append(commander_card.name)

    counts = [single_probability_iteration(decklist, account_generic, mana_target) for _ in range(0, iterations)]
    successes: list = await asyncio.gather(*counts)

    return {'names': commander_names, 'probability': (sum(successes) / iterations), 'mana_target': mana_target}


async def single_probability_iteration(deck_list: DeckList, generic: bool, mana_target: list) -> int:
    """
    Plays a single game.
    :param deck_list: The DeckList object that th game is based on.
    :param generic: True is generic mana is accounted for, False if not.
    :param mana_target: A list containing the mana target.
    :return: If the game was a success return 1, otherwise 0.
    """
    deck_ids = random.sample(deck_list.card_ids, len(deck_list.card_ids))
    hand_ids = []
    draws = sum(mana_target) + 7

    for _ in range(0, draws):
        draw_id = deck_ids[-1]
        hand_ids.append(draw_id)
        deck_ids.pop()

    if success(deck_list, mana_target, hand_ids, generic):
        return 1
    return 0


async def simulate_turns(iterations: int, deck_json: dict,
                         account_generic: bool = True, override_mt: list = None) -> dict:
    """
    Simulates the number of turns it takes to hit your mana target.
    :param iterations: Number of iterations for the simulation.
    :param deck_json: The JSON file of the deck.
    :param account_generic: True (default) if you're looking to hit your commander's manas. False if colours are enough.
    :param override_mt: A custom list of manas if you want to override the commander-based mana target.
    :return: A Dict of commander_names (list), turns (float), mana_target (list).
    """

    decklist = DeckList(deck_json=deck_json)

    if override_mt:
        mana_target = override_mt
    else:
        mana_target = decklist.get_mana_target()

    commander_names = []
    for commander_card in decklist.commanders:
        commander_names.append(commander_card.name)

    counts = [single_turns_iteration(decklist, account_generic, mana_target) for _ in range(0, iterations)]
    turn_counts = await asyncio.gather(*counts)

    return {'names': commander_names, 'turns': (sum(turn_counts) / iterations), 'mana_target': mana_target}


async def single_turns_iteration(deck_list: DeckList, generic: bool, mana_target: list) -> int:
    """
    Plays a single game.
    :param deck_list: The DeckList object that th game is based on.
    :param generic: True is generic mana is accounted for, False if not.
    :param mana_target: A list containing the mana target.
    :return: Turn count at success.
    """
    deck_ids = random.sample(deck_list.card_ids, len(deck_list.card_ids))
    hand_ids = []
    draw_count = 0

    while not success(deck_list, mana_target, hand_ids, generic):
        draw_id = deck_ids[-1]
        hand_ids.append(draw_id)
        deck_ids.pop()
        draw_count += 1
        if draw_count > 50:
            raise RuntimeError("Your simulation has drawn more than 50 cards. "
                               "Are you sure you have enough lands that can produce appropriate colours?")

    return draw_count - 7
