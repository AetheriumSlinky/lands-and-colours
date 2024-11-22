"""Logic functions for queries."""

class ExitException(Exception):
    """
    Used to exit the query.
    """
    pass

class SkipException(Exception):
    """
    Used to clear the query and start over.
    """
    pass

def handle_skip_exit(func):
    """
    User input exit and clear (skip) handling.
    :param func: A function that strictly asks for user input with the input() function.
    :return: Function unless input was 'exit', 'clear' or 'skip'.
    """
    def wrapper(user_input: str):
        if user_input.lower() == 'exit':
            raise ExitException
        elif user_input.lower() in ['clear', 'skip']:
            print("Query cleared. Skipping back to the beginning.")
            raise SkipException
        else:
            func(user_input)
    return wrapper

@handle_skip_exit
def url_query(url: str):
    try:
        print("example:", url)
    except AttributeError as e:
        print(e)
        print("Skipping to first prompt.")
    except ConnectionError as e:
        print(e)
        print("Skipping to first prompt.")

query = input("test this! ")