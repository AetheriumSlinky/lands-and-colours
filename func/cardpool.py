"""Describes cards, card pools and their associated functions."""
from copy import deepcopy

from func.moxfield import DeckList, Card, ManaTarget


class CardPool:
    """
    A pool of objects to draw and subtract from.
    """
    def __init__(self, cards: DeckList):
        # Card objects from the parsed Moxfield DeckList object
        self.cards = cards.cards
        self.lands = cards.lands
        self.target = cards.get_mana_target()
        self.balance = self.target

    def add_card(self, card: Card):
        """
        Adds a Card object to the CardPool object.
        :param card: A Card object to be added.
        """
        self.cards.append(card)
        if card.card_category == 'land':
            self.lands.append(card)

    def remove_card(self, card: Card):
        """
        Removes a Card object from the CardPool object.
        :param card: A Card object to be removed.
        """
        self.cards.remove(card)
        if card.card_category == 'land':
            self.lands.remove(card)

    def subtract_from_balance(self, land: Card) -> bool:
        """
        Subtracts a corresponding Card's mana colour from the ManaTarget. Prioritises mana in 'wubrgc' order.
        :param land: Land Card to subtract from the ManaTarget.
        :return: True if subtraction happened, False if not.
        """
        # Find all coloured identities
        for colour_key in land.colour_identity:
            mana_identities_remaining: int = self.balance.__getattribute__(colour_key)
            current_land_identity: int = land.__getattribute__(colour_key)

            # If land produces the kind of mana that is needed, do subtraction
            if mana_identities_remaining > 0 and current_land_identity > 0:

                # Set new values for the ManaTarget
                self.balance.__setattr__(colour_key, mana_identities_remaining - 1)

                # Subtraction happened so set success to True
                return True

        # If no coloured matches were found subtract from any
        if self.balance.a > 0:
            self.balance.a -= 1

            # Subtraction happened so set success to True
            return True

        # Nothing happened so set success to False
        return False


    def success(self, mana_target: ManaTarget, generic: bool) -> bool:
        """
        Boolean for whether the CardPool object is in success state.
        :param mana_target: A ManaTarget object describing the success state.
        :param generic: True if generic mana is accounted for, False if not.
        :return: True if success, False if not.
        """
        # Set mana target and override generic mana to 0 if generic flag is set to False
        self.balance = deepcopy(mana_target)
        if not generic:
            self.balance.a = 0

        # Land Card objects remaining in the pool
        remaining = deepcopy(self.lands)

        # Temporary storage for subtracting from generic mana later
        storage = []

        # For each land card in the remaining pool...
        for land_card in remaining[:]:
            # Find all cases of lands that have a single colour wubrg+c or a(ny)
            if land_card.get_colours_count() == 1:
                # Attempt to subtract the identity from ManaTarget and return whether it was a success
                subtracted = self.subtract_from_balance(land_card)
                if subtracted:
                    remaining.remove(land_card)
                else:
                    storage.append(land_card)
                    remaining.remove(land_card)

        # For each land card in the remaining pool...
        for land_card in remaining[:]:
            # Find all cases of lands that have a single colour wubrg+c or a(ny)
            if land_card.get_colours_count() == 2:
                # Attempt to subtract the identity from ManaTarget and return whether it was a success
                subtracted = self.subtract_from_balance(land_card)
                if subtracted:
                    remaining.remove(land_card)
                else:
                    storage.append(land_card)
                    remaining.remove(land_card)

        # For each land card in the remaining pool...
        for land_card in remaining[:]:
            # Find all cases of lands that have a single colour wubrg+c or a(ny)
            if land_card.get_colours_count() == 3:
                # Attempt to subtract the identity from ManaTarget and return whether it was a success
                subtracted = self.subtract_from_balance(land_card)
                if subtracted:
                    remaining.remove(land_card)
                else:
                    storage.append(land_card)
                    remaining.remove(land_card)

        # For each land card in the remaining pool...
        for land_card in remaining[:]:
            # Find all cases of lands that have a single colour wubrg+c or a(ny)
            if land_card.get_colours_count() == 4:
                # Attempt to subtract the identity from ManaTarget and return whether it was a success
                subtracted = self.subtract_from_balance(land_card)
                if subtracted:
                    remaining.remove(land_card)
                else:
                    storage.append(land_card)
                    remaining.remove(land_card)

        # For each land card in the remaining pool...
        for land_card in remaining[:]:
            # Find all cases of lands that have a single colour wubrg+c or a(ny)
            if land_card.get_colours_count() == 5:
                # Attempt to subtract the identity from ManaTarget and return whether it was a success
                subtracted = self.subtract_from_balance(land_card)
                if subtracted:
                    remaining.remove(land_card)
                else:
                    storage.append(land_card)
                    remaining.remove(land_card)

        # Subtract remaining identities from generic mana
        for land_card in storage[:]:
            if self.balance.a > 0:
                self.balance.a -= 1
                storage.remove(land_card)

        # If mana target pool is empty it's a success
        if self.balance.total_mana() <= 0:
            return True
        else:
            return False
