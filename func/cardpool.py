"""Describes cards, card pools and their associated functions."""

from copy import deepcopy

from func.moxfield import DeckList, Card


def get_card(cards: DeckList, identifier) -> Card:
    """
    Finds the Card object that corresponds to the identifier.
    :param cards: A DeckList object used as the reference.
    :param identifier: Unique identifier of the Card object.
    :return: The Card object.
    """
    return cards.get_card(identifier)


def success(decklist: DeckList, mana_balance: list, identifiers: list, generic: bool) -> bool:
    """
    Boolean for whether the CardPool object is in success state.
    :param decklist: A DeckList object where all Card objects can be found.
    :param mana_balance: A list describing the available mana.
    :param identifiers: Identifiers of cards in the CardPool object.
    :param generic: True if generic mana is accounted for, False if not.
    :return: True if success, False if not.
    """
    # Copy mana target and override generic mana to 0 if generic flag is set to False
    balance: list = deepcopy(mana_balance)
    if not generic:
        balance[0] = 0

    # Copy the list of identifiers from
    remaining_ids: list = deepcopy(identifiers)

    # Temporary storage for subtracting from generic mana later
    storage = []

    # For each land card in the remaining pool...
    for land_card_id in remaining_ids[:]:
        land_card = get_card(decklist, land_card_id)
        # Find all cases of lands that have a single colour wubrg+c or a(ny)
        if land_card.get_colours_count() == 1:
            # Attempt to subtract the identity from ManaTarget and return whether it was a success
            result = subtract_from_balance(balance, land_card)
            balance = result[0]
            if result[1]:
                remaining_ids.remove(land_card_id)
            else:
                storage.append(land_card_id)
                remaining_ids.remove(land_card_id)

    # For each land card in the remaining pool...
    for land_card_id in remaining_ids[:]:
        land_card = get_card(decklist, land_card_id)
        # Find all cases of lands that have a single colour wubrg+c or a(ny)
        if land_card.get_colours_count() == 2:
            # Attempt to subtract the identity from ManaTarget and return whether it was a success
            result = subtract_from_balance(balance, land_card)
            balance = result[0]
            if result[1]:
                remaining_ids.remove(land_card_id)
            else:
                storage.append(land_card_id)
                remaining_ids.remove(land_card_id)

    # For each land card in the remaining pool...
    for land_card_id in remaining_ids[:]:
        land_card = get_card(decklist, land_card_id)
        # Find all cases of lands that have a single colour wubrg+c or a(ny)
        if land_card.get_colours_count() == 3:
            # Attempt to subtract the identity from ManaTarget and return whether it was a success
            result = subtract_from_balance(balance, land_card)
            balance = result[0]
            if result[1]:
                remaining_ids.remove(land_card_id)
            else:
                storage.append(land_card_id)
                remaining_ids.remove(land_card_id)

    # For each land card in the remaining pool...
    for land_card_id in remaining_ids[:]:
        land_card = get_card(decklist, land_card_id)
        # Find all cases of lands that have a single colour wubrg+c or a(ny)
        if land_card.get_colours_count() == 4:
            # Attempt to subtract the identity from ManaTarget and return whether it was a success
            result = subtract_from_balance(balance, land_card)
            balance = result[0]
            if result[1]:
                remaining_ids.remove(land_card_id)
            else:
                storage.append(land_card_id)
                remaining_ids.remove(land_card_id)

    # For each land card in the remaining pool...
    for land_card_id in remaining_ids[:]:
        land_card = get_card(decklist, land_card_id)
        # Find all cases of lands that have a single colour wubrg+c or a(ny)
        if land_card.get_colours_count() == 5:
            # Attempt to subtract the identity from ManaTarget and return whether it was a success
            result = subtract_from_balance(balance, land_card)
            balance = result[0]
            if result[1]:
                remaining_ids.remove(land_card_id)
            else:
                storage.append(land_card_id)
                remaining_ids.remove(land_card_id)

    # Subtract remaining identities from generic mana
    for land_card_id in storage[:]:
        if balance[0] > 0:
            balance[0] -= 1
            storage.remove(land_card_id)

    # If mana target pool is empty it's a success
    if sum(balance) <= 0:
        return True
    else:
        return False


def subtract_from_balance(balance_list: list, land_card: Card) -> tuple:
    """
    Subtracts mana produced by a land card from the balance.
    :param balance_list: A list of previous mana balance.
    :param land_card: A Card object to subtract from the balance.
    :return: Tuple where first value is the new balance and the second value is boolean for whether subtraction happened.
    """
    new_balance = balance_list

    # No subtraction has happened yet
    subtraction = False

    # Loop over all indices in balance
    for i in range(1, len(balance_list)):

        # If balance has mana left and the land produces the corresponding mana subtract 1
        if (balance_list[i] > 0) and (land_card.mana_produced[i] > 0):
            new_balance[i] -= 1

            # Subtraction happened, stop iterating
            subtraction = True
            break

    # If balance contains generic mana and subtraction hasn't happened yet subtract 1 from generic mana
    if balance_list[0] > 0 and not subtraction:
        new_balance[0] -= 1
        subtraction = True

    return new_balance, subtraction
