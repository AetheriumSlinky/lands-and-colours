"""Main"""

from func.moxfield import MoxfieldError
from func.query import query
from func.query_text import SkipException, ExitException

if __name__ == "__main__":
    print("At any stage:")
    print("The input 'clear' will skip this query to the next one.")
    print("The input 'exit' will exit the program.\n")
    print("REMINDER: this tool assumes you draw one card per turn and play one land per turn.\n"
          "It understands nothing about ramp or filtering. Also MDFCs are ignored (they count as 0 mana spells).")

    while True:
        try:
            query()
        except (SkipException, MoxfieldError, RuntimeError, ConnectionError) as e:
            print(e)
            continue
        except ExitException as e:
            print(e)
            break
