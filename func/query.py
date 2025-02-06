"""Input query main logic function."""

import func.query_text as q_text
import func.probabilities as prob


def query():
    """
    Query.
    """
    deck_json = moxfield_prompt()
    mana_target = define_mana_target_prompt()
    mode = simulation_mode_prompt()
    simulation(deck_json, mana_target, mode)


def moxfield_prompt() -> dict:
    moxfield_url_input = input("\n < Moxfield deck link (url):\n   ")
    deck_json = q_text.json_query(moxfield_url_input)
    return deck_json


def custom_mana_target_prompt() -> bool:
    custom_yes_no = input(
        " < Do you want a custom mana target? "
        "Default: commander mana cost is used. 'Y' or 'N'\n   "
    )
    valid = q_text.valid_custom_mana_target(custom_yes_no)
    return valid


def define_mana_target_prompt() -> list:
    mana_target = []
    valid = custom_mana_target_prompt()
    if valid:
        mana_target_input = input(
            " < Please enter your custom mana target. Format: '#wubrgc', "
            "where '# stands for the number of generic mana and 'c' is colourless, "
            "e.g. {2}{W}{W}{R} is '2wwr' or {1}{C} is '1c'.\n   "
        )
        mana_target = q_text.parse_custom_mana_target(mana_target_input)
    print(" > Mana target processed.\n")
    return mana_target


def simulation_mode_prompt() -> str:
    mode_input = input(
        " < Do you want to simulate the 'probability' of getting your colours on curve "
        "or the number of 'turns' it takes to get your colours or 'both'?\n   "
    )
    mode = q_text.simulation_modes(mode_input)
    return mode


def simulation(deck_json: dict, mana_target: list, mode: str):
    if mode == 'p':
        p = prob.probability_simulation(deck_json=deck_json, target=mana_target)
        cmdr_txt = q_text.commander_names(p['names'])
        mana_target_text = q_text.mana_target_text(p['mana_target'])
        prob_txt = f'''{int(round(p['probability'], 2) * 100)} %'''
        print(f"\n   Commanders: {cmdr_txt}\n   Mana target: {mana_target_text}\n   Probability: {prob_txt}.")


    elif mode == 't':
        t = prob.turn_count_simulation(deck_json=deck_json, target=mana_target)
        cmdr_txt = q_text.commander_names(t['names'])
        mana_target_text = q_text.mana_target_text(t['mana_target'])
        turns_txt = f'''{round(t['turns'], 1)}'''
        print(f"\n   Commanders: {cmdr_txt}\n   Mana target: {mana_target_text}\n   Turn count: {turns_txt}.")

    else:
        p = prob.probability_simulation(deck_json=deck_json, target=mana_target)
        t = prob.turn_count_simulation(deck_json=deck_json, target=mana_target)
        cmdr_txt = q_text.commander_names(p['names'])
        mana_target_text = q_text.mana_target_text(p['mana_target'])
        prob_txt = f'''{int(round(p['probability'], 2) * 100)} %'''
        turns_txt = f'''{round(t['turns'], 1)}'''
        print(f"\n   Commanders: {cmdr_txt}\n   Mana target: {mana_target_text}\n   Probability: {prob_txt} "
              f"| Turn count: {turns_txt}.")
