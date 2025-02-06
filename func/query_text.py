"""Logic functions for queries."""

from func.exceptions import ExitException, SkipException, InvalidInputError
from func.moxfield import Moxfield


def handle_input_exceptions(func):
    """
    Handles 'exit' and 'clear' ('skip') inputs. Throws errors if inputs are not suitable, i.e. not a single string.
    :param func: A function that strictly takes a string argument with the input() function.
    :return: Function unless input was 'exit', 'clear' or 'skip'.
    """
    def wrapper(*args, **kwargs):
        """Wrapper."""
        new_arg = ([arg for arg in args if arg is not None]
                     + [kwarg for kwarg in kwargs.values() if kwarg is not None])

        if len(new_arg) != 1:
            raise ValueError(
                f" > Unexpected number of args or kwargs (was {len(new_arg)}, should be 1). "
                f"The handle_input_exceptions decorator is probably used incorrectly. "
                f"The input should be a single str. Exiting program."
            )

        if not isinstance(new_arg[0], str):
            raise TypeError(
                f" > Invalid data type (was {type(new_arg[0]).__name__}, should be str). "
                f"The handle_input_exceptions decorator is probably used incorrectly. "
                f"The input should be a single str. Exiting program."
            )
        new_arg = ''.join(new_arg).lower()

        while True:

            if new_arg in ['clear', 'skip']:
                raise SkipException(" > Clear command was given.")
            elif new_arg == 'exit':
                raise ExitException(" > Exit command was given.")
            elif not new_arg:
                print(" > Empty input. Please try again or enter 'skip' or 'exit'.")
            else:
                try:
                    return func(new_arg)
                except InvalidInputError as e:
                    print(e)

            new_arg = input(" < Try again:\n   ").lower()

    return wrapper


def json_query(moxfield_url_input: str) -> dict:
    """
    Makes the JSON query based on a given Moxfield url.
    :param moxfield_url_input: The url of the deck.
    :return: JSON file.
    """
    # Moxfield raises its own errors so no input error handling
    if moxfield_url_input.lower() == 'exit':
        raise ExitException(" > Exit command was given.")
    deck_json = Moxfield(moxfield_url_input).moxfield_json
    return deck_json


@handle_input_exceptions
def valid_custom_mana_target(custom_mana_target_input: str) -> bool:
    """
    Checks if user responded yes.
    :param custom_mana_target_input: Input text.
    :return: True if yes or y, False if no or n.
    """
    if custom_mana_target_input.lower() in ['yes', 'y']:
        return True
    elif custom_mana_target_input.lower() in ['no', 'n']:
        return False
    else:
        raise InvalidInputError(" > Input was not 'y' or 'n'. Try again or enter 'skip' or 'exit'.")


@handle_input_exceptions
def parse_custom_mana_target(mana_text_input: str) -> list:
    """
    Constructs the new mana target for overriding the default one.
    :param mana_text_input: A string that describes the new mana target in terms of '#wubrgc'.
    :return: New list of manas.
    """
    mana_target = [0, 0, 0, 0, 0, 0, 0]

    for char in mana_text_input:
        if char.isnumeric():
            mana_target[0] += int(char)
        elif char.lower() in 'wubrgc':
            if char == 'w':
                mana_target[1] += 1
            elif char == 'u':
                mana_target[2] += 1
            elif char == 'b':
                mana_target[3] += 1
            elif char == 'r':
                mana_target[4] += 1
            elif char == 'g':
                mana_target[5] += 1
            elif char == 'c':
                mana_target[6] += 1
        else:
            raise InvalidInputError(" > Erroneous input when defining a custom mana target. "
                                    "Make sure all characters are numbers 1-9 or in 'wubrgca'. "
                                    "Please try again or enter 'skip' or 'exit'.")
    return mana_target


@handle_input_exceptions
def simulation_modes(simulation_mode_input: str) -> str:
    """
    Determines the mode of simulation: probability, turns or both based on user input string
    or raises SkipException if some other word was the input.
    :param simulation_mode_input: User input: probability, turns or both.
    :return: A single letter: p, t or b.
    """
    if simulation_mode_input.lower() == 'probability':
        return 'p'
    elif simulation_mode_input.lower() == 'turns':
        return 't'
    elif simulation_mode_input.lower() == 'both':
        return 'b'
    else:
        raise InvalidInputError(" > Erroneous input when determining simulation mode(s). "
                                "Make sure the input is 'probability', 'turns' or 'both'. "
                                "Please try again or enter 'skip' or 'exit'.")


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


def mana_target_text(mana_target: list) -> str:
    """
    Constructs a printable string of text with all mana types.
    :param mana_target: A list of mana counts.
    :return: Mana target in text format.
    """
    text = (
        f'''generic = {mana_target[0]} | '''
        f'''white = {mana_target[1]} | '''
        f'''blue = {mana_target[2]} | '''
        f'''black = {mana_target[3]} | '''
        f'''red = {mana_target[4]} | '''
        f'''green = {mana_target[5]} | '''
        f'''colourless = {mana_target[6]}'''
    )
    return text
