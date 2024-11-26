"""Input query main logic function."""

import func.query_text as qt
from func.cardpool import ManaTarget


def query():
    """
    Query.
    """
    url_prompt = input("\nMoxfield deck link (url): ")

    deck_json = qt.json_query(url_prompt)

    custom_mt_y_n = input("Do you want a custom mana target? Default: commander mana cost is used. Y/N ")

    if qt.custom_mt_prompt(custom_mt_y_n):

        mana_target_prompt = input(
            "Please enter your custom mana target. Format: 'wubrgca', "
            "where 'c' is colourless and 'a' (any) is generic costs, "
            "e.g. {2}{W}{W}{U} is 'wwuaa' or {1}{C} is 'ca'. ")

        mt = qt.custom_mt_query(mana_target_prompt)

    else:
        mt = ManaTarget()
        print("That's a no. Using default mana target.")

    mode_prompt = input("Do you want to simulate the 'probability' of getting your colours on curve "
                 "or the number of 'turns' it takes to get your colours or 'both'? ")

    mode = qt.simulation_modes_prompt(mode_prompt)

    if mode == 'p':
        p = qt.probability_simulation(deck_json=deck_json, target=mt)
        cmdr_txt = qt.commander_names(p['names'])
        mana_target_text = qt.mana_target_text(p['mana_target'])
        prob_txt = f'''{int(round(p['probability'], 2) * 100)} %'''
        print(f"\nCommanders: {cmdr_txt}\nMana target: {mana_target_text}\nProbability: {prob_txt}.\n")


    elif mode == 't':
        t = qt.turn_count_simulation(deck_json=deck_json, target=mt)
        cmdr_txt = qt.commander_names(t['names'])
        mana_target_text = qt.mana_target_text(t['mana_target'])
        turns_txt = f'''{round(t['turns'], 1)}'''
        print(f"\nCommanders: {cmdr_txt}\nMana target: {mana_target_text}\nTurn count: {turns_txt}.\n")

    elif mode == 'b':
        p = qt.probability_simulation(deck_json=deck_json, target=mt)
        t = qt.turn_count_simulation(deck_json=deck_json, target=mt)
        cmdr_txt = qt.commander_names(p['names'])
        mana_target_text = qt.mana_target_text(p['mana_target'])
        prob_txt = f'''{int(round(p['probability'], 2) * 100)} %'''
        turns_txt = f'''{round(t['turns'], 1)}'''
        print(f"\nCommanders: {cmdr_txt}\nMana target: {mana_target_text}\nProbability: {prob_txt} "
              f"| Turn count: {turns_txt}.\n")

    else:
        print("Something went really wrong.")
