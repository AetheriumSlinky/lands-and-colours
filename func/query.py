"""Input query main logic function."""

import func.query_text as q_text
from func.exceptions import SkipException


def query():
    """
    Query.
    """
    url_prompt = input("\n < Moxfield deck link (url):\n   ")

    deck_json = q_text.json_query(url_prompt)

    custom_mt_y_n = input(" < Do you want a custom mana target? Default: commander mana cost is used. Y/N\n   ")

    if q_text.custom_mt_prompt(custom_mt_y_n):

        mana_target_prompt = input(
            " < Please enter your custom mana target. Format: '#wubrgc', "
            "where '# stands for the number of generic mana and 'c' is colourless, "
            "e.g. {2}{W}{W}{U} is '2ww' or {1}{C} is '1c'.\n   ")

        mt = q_text.custom_mt_query(mana_target_prompt)

        print(" > Mana target processed.")

    else:
        mt = []
        print(" > That's a no. Using default mana target.\n")

    mode_prompt = input(" < Do you want to simulate the 'probability' of getting your colours on curve "
                 "or the number of 'turns' it takes to get your colours or 'both'?\n   ")

    mode = q_text.simulation_modes_prompt(mode_prompt)

    if mode == 'p':
        p = q_text.probability_simulation(deck_json=deck_json, target=mt)
        cmdr_txt = q_text.commander_names(p['names'])
        mana_target_text = q_text.mana_target_text(p['mana_target'])
        prob_txt = f'''{int(round(p['probability'], 2) * 100)} %'''
        print(f"\n   Commanders: {cmdr_txt}\n   Mana target: {mana_target_text}\n   Probability: {prob_txt}.")


    elif mode == 't':
        t = q_text.turn_count_simulation(deck_json=deck_json, target=mt)
        cmdr_txt = q_text.commander_names(t['names'])
        mana_target_text = q_text.mana_target_text(t['mana_target'])
        turns_txt = f'''{round(t['turns'], 1)}'''
        print(f"\n   Commanders: {cmdr_txt}\n   Mana target: {mana_target_text}\n   Turn count: {turns_txt}.")

    elif mode == 'b':
        p = q_text.probability_simulation(deck_json=deck_json, target=mt)
        t = q_text.turn_count_simulation(deck_json=deck_json, target=mt)
        cmdr_txt = q_text.commander_names(p['names'])
        mana_target_text = q_text.mana_target_text(p['mana_target'])
        prob_txt = f'''{int(round(p['probability'], 2) * 100)} %'''
        turns_txt = f'''{round(t['turns'], 1)}'''
        print(f"\n   Commanders: {cmdr_txt}\n   Mana target: {mana_target_text}\n   Probability: {prob_txt} "
              f"| Turn count: {turns_txt}.")

    else:
        raise SkipException(" > Something went really wrong while calculating simulations.")
