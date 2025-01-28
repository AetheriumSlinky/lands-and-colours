"""Logic functions for queries."""

import asyncio

from func.moxfield import parse_moxfield_url, moxfield_api_request, ManaTarget
from func.probabilities import simulate_turns, simulate_probability


class ExitException(Exception):
    """
    Used to exit the query.
    """
    pass


class SkipException(Exception):
    """
    Used to clear the query and start over.
    """
    pass


def handle_skip_exit(func):
    """
    User input exit and clear (skip) handling.
    :param func: A function that strictly asks for user input with the input() function.
    :return: Function unless input was 'exit', 'clear' or 'skip'.
    """
    def wrapper(user_input: str):
        """Wrapper."""
        if not user_input:
            raise SkipException("No input.")
        elif user_input.lower() in ['clear', 'skip']:
            raise SkipException("Clear command was given.")
        elif user_input.lower() == 'exit':
            raise ExitException("Exit command was given.")
        else:
            return func(user_input)
    return wrapper


@handle_skip_exit
def json_query(url) -> dict:
    """
    Makes the JSON query based on a given Moxfield url.
    :param url: The url of the deck.
    :return: JSON file.
    """
    deck_json = moxfield_api_request(parse_moxfield_url(url=url))
    return deck_json


@handle_skip_exit
def custom_mt_prompt(text: str) -> bool:
    """
    Checks if user responded yes.
    :param text: Input text.
    :return: True if yes or y, otherwise False.
    """
    if text.lower() in ['yes', 'y']:
        return True
    return False


@handle_skip_exit
def custom_mt_query(mana_input: str) -> ManaTarget:
    """
    Constructs the new ManaTarget for overriding the default one
    or raises SkipException if an erroneous input was given.
    :param mana_input: A string that describes the new ManaTarget in terms of 'wubrgca'.
    :return: New ManaTarget.
    """
    mana_target_obj = ManaTarget()

    for char in mana_input:
        if char.lower() not in 'wubrgca':
            raise SkipException("Erroneous input when defining a custom mana target.")
        else:
            prev = mana_target_obj.__getattribute__(char)
            mana_target_obj.__setattr__(char, prev + 1)

    print("Mana target processed.")
    return mana_target_obj


@handle_skip_exit
def simulation_modes_prompt(mode: str) -> str:
    """
    Determines the mode of simulation: probability, turns or both based on user input string
    or raises SkipException if some other word was the input.
    :param mode: User input: probability, turns or both.
    :return: A single letter: p, t or b.
    """
    if mode == 'probability':
        return 'p'
    elif mode == 'turns':
        return 't'
    elif mode == 'both':
        return 'b'
    else:
        raise SkipException("Erroneous input when determining simulation mode(s).")


def probability_simulation(deck_json: dict, target: ManaTarget) -> dict:
    """
    Calls the simulate_probability function. If ManaTarget has custom settings it calls the function with those parameters.
    :param deck_json: The deck's JSON file.
    :param target: ManaTarget.
    :return: Default probability if ManaTarget was default, override if a custom ManaTarget was provided.
    """
    if not target.total_mana() == 0:
        return simulate_probability(iterations=1000, deck_json=deck_json, override_mt=target)
    return simulate_probability(iterations=1000, deck_json=deck_json)


def turn_count_simulation(deck_json: dict, target: ManaTarget) -> dict:
    """
    Calls the simulate_turns function. If ManaTarget has custom settings it calls the function with those parameters.
    :param deck_json: The deck's JSON file.
    :param target: ManaTarget.
    :return: Default probability if ManaTarget was default, override if a custom ManaTarget was provided.
    """
    if not target.total_mana() == 0:
        return asyncio.run(simulate_turns(iterations=1000, deck_json=deck_json, override_mt=target))
    return asyncio.run(simulate_turns(iterations=1000, deck_json=deck_json))


def commander_names(names: list) -> str:
    """
    Constructs printable string of text with all commander names.
    :param names: A list of names.
    :return: Names in text format.
    """
    name_text = f"{names[0]}"
    if len(names) > 1:
        for name in range(1, len(names)):
            name_text += f" and {name}"
    return name_text


def mana_target_text(mana_target: ManaTarget) -> str:
    """
    Constructs a printable string of text with all mana types.
    :param mana_target: A ManaTarget object.
    :return: Mana target in text format.
    """
    text = (
        f'''generic = {mana_target.a} | '''
        f'''white = {mana_target.w} | '''
        f'''blue = {mana_target.u} | '''
        f'''black = {mana_target.b} | '''
        f'''red = {mana_target.r} | '''
        f'''green = {mana_target.g} | '''
        f'''colourless = {mana_target.c}'''
    )
    return text
