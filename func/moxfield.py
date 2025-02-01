"""Parse decklist into Card objects and other information starting from url."""

import time
import requests
import json

from func.exceptions import MoxfieldError, UserAgentError
from user_agent import read_ua


class Card:
    """
    A card item with characteristics.
    """
    def __init__(self, identifier: int, card_json=None):

        # Provide a dict containing the card's JSON
        self.__card_json = card_json

        # Properties that are accessible
        self.identifier = identifier
        self.name = ''
        self.card_category = ''
        self.colour_identity = ''
        self.mana_value = 0
        self.mana_cost = {'a': 0, 'w': 0, 'u': 0, 'b': 0, 'r': 0, 'g': 0, 'c': 0}
        self.mana_produced = [0, 0, 0, 0, 0, 0, 0]

        # Finally, parse card
        self.__parse_card(identifier)

    def __str__(self):
        return f"Attributes: {self.__dict__}"

    def __set_mana_to_one(self, colour_key: str):
        """
        Sets the correct mana production for the card.
        :param colour_key: A single character string from wubgrca.
        """
        for index, colour in enumerate('awubrgc'):
            if colour_key == colour:
                self.mana_produced[index] = 1

    def __parse_card(self, identifier: int):
        """
        Parses the card's JSON into characteristics and empties JSON.
        :param identifier: The identifier of the Card object or raises ValueError if no json was present.
        """
        # Make sure JSON exists
        if self.__card_json:

            self.name = self.__card_json['name']
            self.identifier = identifier

            # If the card is an MDFC just... ignore it, kinda - it's a nonland
            if '//' in self.__card_json['type_line']:
                self.colour_identity = ''.join(self.__card_json['color_identity']).lower()
                self.card_category = 'nonland'

            # Other lands get categorised as lands
            elif 'Land' in self.__card_json['type_line']:
                self.card_category = 'land'

                # If the oracle text contains keywords for any colour or a fetch set identity to wubrg
                if 'any color' in self.__card_json['oracle_text'] or 'acrifice' in self.__card_json['oracle_text']:
                    self.colour_identity = 'wubrg'
                    for colour_key in self.colour_identity:
                        self.__set_mana_to_one(colour_key)

                # If the JSON identity is empty we assume the land can produce colourless mana (cue Maze of Ith...)
                elif ''.join(self.__card_json['color_identity']) == '':
                    self.colour_identity = 'c'
                    self.__set_mana_to_one('c')

                elif 'Basic' in self.__card_json['type_line']:
                    self.colour_identity = ''.join(self.__card_json['color_identity']).lower()
                    for colour_key in self.colour_identity:
                        self.__set_mana_to_one(colour_key)

                # Catch all other identities such as duals
                else:
                    self.colour_identity = ''.join(self.__card_json['color_identity']).lower()
                    for colour_key in self.colour_identity:
                        self.__set_mana_to_one(colour_key)

            # Catch nonlands
            else:
                self.colour_identity = ''.join(self.__card_json['color_identity']).lower()

                # If colour identity is empty (such as colourless Artifacts) give it the 'c' identity
                if not self.colour_identity:
                    self.colour_identity = 'c'

                self.card_category = 'nonland'

            # Further sort nonlands' costs but exclude MDFCs again - they're now nonlands with no cost
            if (self.card_category == 'nonland') and ('//' not in self.__card_json['type_line']):

                # Loop through all colour identity characters in the mana cost
                for character in self.__card_json['mana_cost']:

                    # Increment mana_cost for each coloured mana
                    if character.lower() in 'wubrgc':
                        self.mana_cost[character.lower()] += 1

                    # Increment generic mana equal to generic mana in mana cost
                    # This breaks at mana costs above 9
                    elif character.isnumeric():
                        self.mana_cost['a'] += int(character)

            # Set the total mana value of the card
            self.mana_value = self.__card_json['cmc']

            # Clear JSON because it's rather heavy and there's no reason to keep it around anymore
            self.__card_json = None

        # If no JSON is provided, but you still try to parse the card, throw an error
        else:
            raise AttributeError('No JSON file was found. Card object characteristics cannot be parsed.')

    def get_colours_count(self) -> int:
        """
        Determine total number of different kinds of mana this object can produce.
        For example: wu land has a value of 2, a basic has a value of 1, rainbows have a value of 5 etc.
        :return: Number of a land's colour identities.
        """
        return sum(self.mana_produced)


class DeckList:
    """
    By default, an empty object describing the characteristics of a deck.
    If JSON is provided the object is automatically parsed and JSON cleared at the end.
    """
    def __init__(self, deck_json=None):
        self.__deck_json = {}
        self.commanders = []
        self.cards = []
        self.card_ids = []
        self.land_ids = []

        # If JSON is present parse it straight away
        if deck_json:
            self.__deck_json = deck_json
            self.__parse_commander_json()
            self.__parse_deck_json()
            self.__deck_json = None

    def __str__(self):
        return f"Attributes: {self.__dict__}"

    def __parse_commander_json(self):
        """
        Parses the JSON file into commander Card objects and appends them to the DeckList object.
        """
        for card_index, cardname in enumerate(list(self.__deck_json['commanders'].keys())):
            card = Card(card_index, self.__deck_json['commanders'][f'{cardname}']['card'])
            self.commanders.append(card)

    def __parse_deck_json(self):
        """
        Parses the JSON file into individual Card objects and appends them to the DeckList object.
        """
        for card_index, cardname in enumerate(list(self.__deck_json['mainboard'].keys())):
            for count in range(0, self.__deck_json['mainboard'][f'{cardname}']['quantity']):
                card = Card(card_index, self.__deck_json['mainboard'][f'{cardname}']['card'])
                self.cards.append(card)
                self.card_ids.append(card_index)
                if card.card_category == 'land':
                    self.land_ids.append(card_index)

    def get_mana_target(self) -> list:
        """
        Gets a list of manas based on commander Card objects in the DeckList.
        :return: A list describing the mana required.
        """
        manas = [0, 0, 0, 0, 0, 0, 0]

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

                    # Actually change the mana target list's values
                    if colour_key == 'w':
                        manas[1] += commander.mana_cost[colour_key]
                    elif colour_key == 'u':
                        manas[2] += commander.mana_cost[colour_key]
                    elif colour_key == 'b':
                        manas[3] += commander.mana_cost[colour_key]
                    elif colour_key == 'r':
                        manas[4] += commander.mana_cost[colour_key]
                    elif colour_key == 'g':
                        manas[5] += commander.mana_cost[colour_key]
                    elif colour_key == 'c':
                        manas[6] += commander.mana_cost[colour_key]

        # Compare all stored generic costs and pick the bigger one, then subtract all coloured costs
        manas[0] = int(max(mana_values.values()) - sum(manas))

        # In some hybrid mana cases it's possible that generic mana is set to negative so just fix that
        if manas[0] < 0:
            manas[0] = 0

        return manas

    def get_card(self, identifier: int) -> Card:
        """
        Finds the corresponding Card object based on its identifier.
        :param identifier: The identifier number of a Card object.
        :return: The Card object.
        """
        card_index = self.card_ids.index(identifier)
        card = self.cards[card_index]
        return card


def parse_moxfield_url(url: str) -> str:
    """
    Converts a regular deck link into an API call url.
    :param url: Regular deck url.
    :return: API call url.
    """
    if 'moxfield' not in url:
        raise MoxfieldError("Not a Moxfield link.")
    deck_id = url[url.find('decks/') + len('decks/'):]
    return f'https://api.moxfield.com/v2/decks/all/{deck_id}'


def moxfield_api_request(api_url: str) -> dict:
    """
    Makes an API request to Moxfield for a deck's JSON.
    :param api_url: The url to make the API call to.
    :return: JSON file.
    """
    # DON'T MAKE TOO MANY API CALLS PER SECOND PLS
    time.sleep(0.2)
    try:
        moxfield_response = requests.get(
            headers={'User-Agent': read_ua()},
            url=api_url).text
        if 'You are unable to access' in moxfield_response:
            raise UserAgentError("You did not provide a whitelisted User-Agent.")
        json_file = json.loads(moxfield_response)
        try:
            if len(json_file['commanders']) == 0:
                raise MoxfieldError("Your deck doesn't have any commanders, i.e. it is not a commander deck.")
            return json_file
        except KeyError:
            raise MoxfieldError("Your deck is probably set to private or it doesn't exist.")
    except (NameError, FileNotFoundError):
        raise UserAgentError("User-Agent string or file not set properly. Modify user_agent.py, please.")
    except ConnectionError as e:
        raise ConnectionError(f"Connection error. Here's the error code: {e}")
