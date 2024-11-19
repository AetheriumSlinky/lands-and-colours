"""Describes cards, card pools and their associated functions."""

from func.moxfield import DeckList, Card, ManaTarget


class CardPool:
    """
    A pool of objects to draw and subtract from.
    """
    def __init__(self, cards: DeckList):
        # Card objects from the parsed Moxfield DeckList object
        self.cards = cards.cards

        # A ManaTarget object describing the success state
        self.target = cards.target

    def add_card(self, card: Card):
        """
        Adds a Card object to the CardPool object.
        :param card: A Card object to be added.
        """
        self.cards.append(card)

    def remove_card(self, card: Card):
        """
        Removes a Card object from the CardPool object.
        :param card: A Card object to be removed.
        """
        self.cards.remove(card)

    def get_land_identities(self) -> list:
        """
        A list of the colour identities of lands in the CardPool object
        as permutations of 'wubrgca', where c stands for colourless and a stands for any (generic).
        Examples of identities: 'w' or 'ubr' or 'c' or 'a'.
        :return: List of colour identities.
        """
        identities = []
        for card in self.cards:
            if card.card_category == 'land':
                identities.append(card.colour_identity)
        return identities

    def success(self, mana_target: ManaTarget, generic: bool) -> bool:
        """
        Boolean for whether the CardPool object is in success state.
        :param mana_target: A ManaTarget object describing the success state.
        :param generic: True if generic mana is accounted for, False if not.
        :return: True if success, False if not.
        """
        # Current state of desired colours to subtract from as described by the ManaTarget parameter
        state = {'w': mana_target.w, 'u': mana_target.u, 'b': mana_target.b,
                 'r': mana_target.r, 'g': mana_target.g, 'c': mana_target.c,
                 'a': mana_target.a}

        # Override generic mana to zero if generic is set to False
        if not generic:
            state['a'] = 0

        # Land colour identities remaining in the pool
        remaining: list = self.get_land_identities()

        # Temporary storage for subtracting from generic mana later
        storage: list = []

        # For each colour identity in the remaining pool...
        for colour_id in remaining[:]:
            # Find all cases of identities that have a single colour wubrg+c and a(ny)
            if len(colour_id) == 1:
                # And state must still have identities of that type left
                if state[colour_id] > 0:
                    # Remove an identity from the state
                    state[colour_id] -= 1
                # Remove all single coloured sources from list of remaining sources
                else:
                    storage.append(colour_id)
                remaining.remove(colour_id)

        # For each colour identity in the remaining pool...
        for colour_id in remaining[:]:
            # Find all cases of identities that have two colours
            if len(colour_id) == 2:
                if state[colour_id[0]] > 0:
                    state[colour_id[0]] -= 1
                elif state[colour_id[1]] > 0:
                    state[colour_id[1]] -= 1
                else:
                    storage.append(colour_id)
                remaining.remove(colour_id)

        # For each colour identity in the remaining pool...
        for colour_id in remaining[:]:
            # Find all cases of identities that have three colours
            if len(colour_id) == 3:
                if state[colour_id[0]] > 0:
                    state[colour_id[0]] -= 1
                elif state[colour_id[1]] > 0:
                    state[colour_id[1]] -= 1
                elif state[colour_id[2]] > 0:
                    state[colour_id[2]] -= 1
                else:
                    storage.append(colour_id)
                remaining.remove(colour_id)

        # For each colour identity in the remaining pool...
        for colour_id in remaining[:]:
            # Find all cases of identities that have four colours
            if len(colour_id) == 4:
                # We just remove these because no such thing exists - pointless to check these
                storage.append(colour_id)
                remaining.remove(colour_id)

        # For each colour identity in the remaining pool...
        for colour_id in remaining[:]:
            # Find all cases of identities that have five colours
            if len(colour_id) == 5:
                if state[colour_id[0]] > 0:
                    state[colour_id[0]] -= 1
                elif state[colour_id[1]] > 0:
                    state[colour_id[1]] -= 1
                elif state[colour_id[2]] > 0:
                    state[colour_id[2]] -= 1
                elif state[colour_id[3]] > 0:
                    state[colour_id[3]] -= 1
                elif state[colour_id[4]] > 0:
                    state[colour_id[4]] -= 1
                else:
                    storage.append(colour_id)
                remaining.remove(colour_id)

        # Subtract remaining identities from generic mana
        for colour_id in storage[:]:
            if state["a"] > 0:
                state["a"] -= 1
                storage.remove(colour_id)

        # If mana target pool is empty it's a success
        if sum(state.values()) <= 0:
            return True
        else:
            return False