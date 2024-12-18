"""Parse decklist into Card objects and other information starting from url."""

import time
import requests
import json


class MoxfieldError(Exception):
    """
    Used to raise Moxfield related errors.
    """
    pass


class ManaTarget:
    """
    Mana target object. Number of each colour. Attributes: wubrg plus c(olourless) and a(ny i.e. generic).
    """
    def __init__(self, w=0, u=0, b=0, r=0, g=0, c=0, a=0):
        self.w = w
        self.u = u
        self.b = b
        self.r = r
        self.g = g
        self.c = c
        self.a = a

    def __str__(self):
        return f"Attributes: {self.__dict__}"

    def total_mana(self) -> int:
        """
        Determines how much mana in total is in the ManaTarget object. Think of as len() for this object.
        :return: Total number of manas.
        """
        mana_sum = self.w + self.u + self.b + self.r + self.g + self.c + self.a
        return mana_sum


class Card:
    """
    A card item with characteristics. Initially empty unless the parse function is used.
    Beware of trying to parse an empty JSON file.
    """
    def __init__(self, card_json=None):
        self.name = ''
        self.card_json = card_json
        self.card_category = ''
        self.colour_identity = ''
        self.mana_value = 0
        self.mana_cost = {'w': 0, 'u': 0, 'b': 0, 'r': 0, 'g': 0, 'c': 0, 'a': 0}

        # These are for lands producing mana
        self.w = 0
        self.u = 0
        self.b = 0
        self.r = 0
        self.g = 0
        self.c = 0

    def __str__(self):
        return f"Attributes: {self.__dict__}"

    def parse_card(self):
        """
        Parses the card's JSON into characteristics and empties JSON.
        """
        # Make sure JSON exists
        if self.card_json:

            self.name = self.card_json['name']

            # If the card is an MDFC just... ignore it, kinda - it's a nonland
            if '//' in self.card_json['type_line']:
                self.colour_identity = ''.join(self.card_json['color_identity']).lower()
                self.card_category = 'nonland'

            # Other lands get categorised as lands
            elif 'Land' in self.card_json['type_line']:
                self.card_category = 'land'

                # If the oracle text contains keywords for any colour or a fetch set identity to wubrg
                if 'any color' in self.card_json['oracle_text'] or 'acrifice' in self.card_json['oracle_text']:
                    self.colour_identity = 'wubrg'
                    for colour_key in self.colour_identity:
                        self.__setattr__(colour_key, 1)

                # If the JSON identity is empty we assume the land can produce colourless mana (cue Maze of Ith...)
                elif ''.join(self.card_json['color_identity']) == '':
                    self.colour_identity = 'c'
                    self.c = 1

                elif 'Basic' in self.card_json['type_line']:
                    self.colour_identity = ''.join(self.card_json['color_identity']).lower()
                    for colour_key in self.colour_identity:
                        self.__setattr__(colour_key, 1)

                # Catch all other identities such as duals
                else:
                    self.colour_identity = ''.join(self.card_json['color_identity']).lower()
                    for colour_key in self.colour_identity:
                        self.__setattr__(colour_key, 1)

            # Catch nonlands
            else:
                self.colour_identity = ''.join(self.card_json['color_identity']).lower()

                # If colour identity is empty (such as colourless Artifacts) give it the 'c' identity
                if not self.colour_identity:
                    self.colour_identity = 'c'

                self.card_category = 'nonland'

            # Further sort nonlands' costs but exclude MDFCs again - they're now nonlands with no cost
            if (self.card_category == 'nonland') and ('//' not in self.card_json['type_line']):

                # Loop through all colour identity characters in the mana cost
                for character in self.card_json['mana_cost']:

                    # Increment mana_cost for each coloured mana
                    if character.lower() in 'wubrgc':
                        self.mana_cost[character.lower()] += 1

                    # Increment generic mana equal to generic mana in mana cost
                    # This breaks at mana costs above 9
                    elif character.isnumeric():
                        self.mana_cost['a'] += int(character)

            # Set the total mana value of the card
            self.mana_value = self.card_json['cmc']

            # Clear JSON because it's rather heavy and there's no reason to keep it around anymore
            self.card_json = None

        # If no JSON is provided, but you still try to parse the card, throw an error
        else:
            raise AttributeError('No JSON file was provided. Card object characteristics cannot be parsed.')

    def get_colours_count(self) -> int:
        """
        Determine total number of different kinds of mana this object can produce.
        For example: wu land has a value of 2, a basic has a value of 1, rainbows have a value of 5 etc.
        :return: Number of a land's colour identities.
        """
        identity_count = self.w + self.u + self.b + self.r + self.g + self.c
        return identity_count


class DeckList:
    """
    By default, an empty object describing the characteristics of a deck.
    If JSON is provided the object is automatically parsed and JSON cleared at the end.
    """
    def __init__(self, deck_json=None):
        self.deck_json = {}
        self.commanders = []
        self.cards = []
        self.lands = []

        # If JSON is present parse it straight away
        if deck_json:
            self.deck_json = deck_json
            self.parse_commander_json()
            self.parse_deck_json()
            self.deck_json = None

    def __str__(self):
        return f"Attributes: {self.__dict__}"

    def parse_commander_json(self):
        """
        Parses the JSON file into commander Card objects and appends them to the DeckList object.
        """
        for cardname in list(self.deck_json['commanders'].keys()):
            card = Card(self.deck_json['commanders'][f'{cardname}']['card'])
            card.parse_card()
            self.commanders.append(card)

    def parse_deck_json(self):
        """
        Parses the JSON file into individual Card objects and appends them to the DeckList object.
        """
        for cardname in list(self.deck_json['mainboard'].keys()):
            for count in range(0, self.deck_json['mainboard'][f'{cardname}']['quantity']):
                card = Card(self.deck_json['mainboard'][f'{cardname}']['card'])
                card.parse_card()
                self.cards.append(card)
                if card.card_category == 'land':
                    self.lands.append(card)

    def get_mana_target(self) -> ManaTarget:
        """
        Gets the ManaTarget object based on commander Card objects in the DeckList.
        :return: ManaTarget object.
        """
        manas = ManaTarget()

        # This dict is for partners and backgrounds etc
        mana_values = {0: 0, 1: 0}

        # Loop through each commander Card object
        for index, commander in enumerate(self.commanders):

            # Save the mana value of the commander
            mana_values[index] = commander.mana_value

            # Loop through each colour character in the mana cost
            for colour_key in commander.mana_cost.keys():

                # Exclude generic mana
                if colour_key != 'a':

                    # Actually change the ManaTarget object's values
                    prev = manas.__getattribute__(colour_key)
                    manas.__setattr__(colour_key, max(commander.mana_cost[colour_key], prev))

        # Compare all stored generic costs and pick the bigger one, then subtract all coloured costs
        manas.a = int(max(mana_values.values()) - manas.total_mana())

        # In some hybrid mana cases it's possible that generic mana is set to negative so just fix that
        if manas.a < 0:
            manas.a = 0

        return manas


def parse_moxfield_url(url: str) -> str:
    """
    Converts a regular deck link into an API call url.
    :param url: Regular deck url.
    :return: API call url.
    """
    if 'moxfield' not in url:
        raise MoxfieldError("Not a Moxfield link. Try again.")
    deck_id = url[url.find('decks/') + len('decks/'):]
    return f'https://api.moxfield.com/v2/decks/all/{deck_id}'


def moxfield_api_request(api_url: str) -> dict:
    """
    Makes an API request to Moxfield for a deck's JSON.
    :param api_url: The url to make the API call to.
    :return: JSON file.
    """
    # DON'T MAKE TOO MANY API CALLS PER SECOND PLS
    time.sleep(1)
    try:
        moxfield_response = requests.get(
            headers={'User-Agent': 'LandsAndColoursTool/0.1.0'},
            url=api_url).text
        json_file = json.loads(moxfield_response)
        try:
            if len(json_file['commanders']) == 0:
                raise MoxfieldError("Your deck doesn't have any commanders, i.e. it is not a commander deck.")
            return json_file
        except KeyError:
            raise MoxfieldError("Your deck is probably set to private or it doesn't exist.")
    except ConnectionError as e:
        raise ConnectionError(f"Connection error. Here's the error code: {e}")
