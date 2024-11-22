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
        mt = ManaTarget()
        mt_flag = False
        url = input("Moxfield deck link (url): ")

        if url.lower() == 'clear' or not url:
            print("Skipping to first prompt.")
            continue
        elif url.lower() == 'exit':
            break

        try:
            deck_json = moxfield_api_request(parse_moxfield_url(url=url))
        except AttributeError as e:
            print(e)
            print("Skipping to first prompt.")
            continue
        except ConnectionError as e:
            print(e)
            print("Skipping to first prompt.")
            continue

        custom = input("Do you want a custom mana target? Default: commander mana cost is used. Y/N ")

        if custom.lower() == 'clear':
            print("Skipping to first prompt.")
            continue
        elif custom.lower() == 'exit':
            break
        elif custom.lower() in ['y', 'yes']:
            mt_input = input(
                "Please enter your custom mana target. Format: 'wubrgca', "
                "where 'c' is colourless and 'a' (any) is generic costs, "
                "e.g. {2}{W}{W}{U} is 'wwuaa' or {1}{C} is 'ca'. ")
            if not mt_input:
                print("No input. Using default mana target.")
                pass
            elif mt_input.lower() == 'clear':
                print("Skipping to first prompt.")
                continue
            elif mt_input.lower() == 'exit':
                break
            else:
                for char in mt_input:
                    if char.lower() not in 'wubrgca':
                        print("Erroneous mana target. Using default mana target.")
                        mt_flag = False
                        break
                    else:
                        prev = mt.__getattribute__(char)
                        mt.__setattr__(char, prev + 1)
                        mt_flag = True
                if mt_flag:
                    print("Mana target processed.")
        else:
            print("That's a no. Using default mana target.")
            pass

        mode = input("Do you want to simulate the 'probability' of getting your colours on curve "
                     "or the number of 'turns' it takes to get your colours or 'both'? ")

        if mode == 'clear':
            print("Skipping to first prompt.")
            continue

        elif mode == 'exit':
            break

        elif mode == 'probability':
            if mt_flag:
                p_results = simulate_probability(iterations=1000, deck_json=deck_json, override_mt=mt)
            else:
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
            if mt_flag:
                try:
                    t_results = simulate_turns(iterations=1000, deck_json=deck_json, override_mt=mt)
                except RuntimeError as e:
                    print(e)
                    print("Skipping to first prompt.")
                    continue
            else:
                try:
                    t_results = simulate_turns(iterations=1000, deck_json=deck_json, account_generic=False)
                except RuntimeError as e:
                    print(e)
                    print("Skipping to first prompt.")
                    continue

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
            if mt_flag:
                try:
                    p_results = simulate_probability(iterations=1000, deck_json=deck_json, override_mt=mt)
                    t_results = simulate_turns(iterations=1000, deck_json=deck_json, override_mt=mt)
                except RuntimeError as e:
                    print(e)
                    print("Skipping to first prompt.")
                    continue
            else:
                try:
                    p_results = simulate_probability(iterations=1000, deck_json=deck_json, account_generic=False)
                    t_results = simulate_turns(iterations=1000, deck_json=deck_json, account_generic=False)
                except RuntimeError as e:
                    print(e)
                    print("Skipping to first prompt.")
                    continue

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
