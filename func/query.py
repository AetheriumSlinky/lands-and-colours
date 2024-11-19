"""Query (input)"""

from func.moxfield import parse_moxfield_url, moxfield_api_request, ManaTarget
from func.probabilities import simulate_turns, simulate_probability

def query():
    """
    Query loop.
    """
    print("At any stage:")
    print("The input 'clear' will skip this query to the next one.")
    print("The input 'exit' will exit the program.\n")

    while True:
        deck_json = {}
        url = input("Moxfield deck link (url): ")

        if url == 'clear' or not url:
            print("Skipping to first prompt.")
            continue
        elif url == 'exit':
            break

        try:
            deck_json = moxfield_api_request(parse_moxfield_url(url=url))
        except Exception:
            print("Invalid deck link, deck set to private, connection error or some other problem. Try again.")
            continue

        mode = input("Do you want to simulate the 'probability' of getting your colours on curve "
                     "or the number of 'turns' it takes to get your colours or 'both'? ")

        if mode == 'clear':
            print("Skipping to first prompt.")
            continue

        elif mode == 'exit':
            break

        elif mode == 'probability':
            p_results = simulate_probability(iterations=1000, deck_json=deck_json, account_generic=False)

            if len(p_results['names']) == 2:
                cmdr_names = f'''{p_results['names'][0]} and {p_results['names'][1]}'''
            else:
                cmdr_names = f'''{p_results['names'][0]}'''

            mana_target = (
                f'''generic = {p_results['mana_target'].a}, '''
                f'''white = {p_results['mana_target'].w}, '''
                f'''blue = {p_results['mana_target'].u}, '''
                f'''black = {p_results['mana_target'].b}, '''
                f'''red = {p_results['mana_target'].r}, '''
                f'''green = {p_results['mana_target'].g}, '''
                f'''colourless = {p_results['mana_target'].c}'''
            )

            prob = f'''{int(round(p_results['probability'], 2) * 100)} %'''

            print(f"\nCommanders: {cmdr_names}\nMana target: {mana_target}\nProbability: {prob}.\n")

        elif mode == 'turns':
            t_results = simulate_turns(iterations=1000, deck_json=deck_json, account_generic=False)

            if len(t_results['names']) == 2:
                cmdr_names = f'''{t_results['names'][0]} and {t_results['names'][1]}'''
            else:
                cmdr_names = f'''{t_results['names'][0]}'''

            mana_target = (
                f'''generic = {t_results['mana_target'].a}, '''
                f'''white = {t_results['mana_target'].w}, '''
                f'''blue = {t_results['mana_target'].u}, '''
                f'''black = {t_results['mana_target'].b}, '''
                f'''red = {t_results['mana_target'].r}, '''
                f'''green = {t_results['mana_target'].g}, '''
                f'''colourless = {t_results['mana_target'].c}'''
            )

            turns = f'''{round(t_results['turns'], 1)}'''

            print(f"\nCommanders: {cmdr_names}\nMana target: {mana_target}\nTurn count: {turns}.\n")

        elif mode == 'both':
            p_results = simulate_probability(iterations=1000, deck_json=deck_json, account_generic=False)
            t_results = simulate_turns(iterations=1000, deck_json=deck_json, account_generic=False)

            if len(p_results['names']) == 2:
                cmdr_names = f'''{p_results['names'][0]} and {p_results['names'][1]}'''
            else:
                cmdr_names = f'''{p_results['names'][0]}'''

            mana_target = (
                f'''generic = {p_results['mana_target'].a}, '''
                f'''white = {p_results['mana_target'].w}, '''
                f'''blue = {p_results['mana_target'].u}, '''
                f'''black = {p_results['mana_target'].b}, '''
                f'''red = {p_results['mana_target'].r}, '''
                f'''green = {p_results['mana_target'].g}, '''
                f'''colourless = {p_results['mana_target'].c}'''
            )

            prob = f'''{int(round(p_results['probability'], 2) * 100)} %'''
            turns = f'''{round(t_results['turns'], 1)}'''

            print(f"\nCommanders: {cmdr_names}\nMana target: {mana_target}\nProbability: {prob} "
                  f"| Turn count: {turns}.\n")

        else:
            print("Skipping to first prompt.")
            continue
