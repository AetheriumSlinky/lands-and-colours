"""Main."""

from func.exceptions import SkipException, ExitException, MoxfieldError, UserAgentError
from func.query import query


def main():
    """
    Main.
    """
    print(" > At any stage:")
    print(" > The input 'clear' will skip this query to the next one.")
    print(" > The input 'exit' will exit the program.\n")
    print(" > REMINDER: this tool assumes you draw one card per turn and play one land per turn.\n"
          " > It understands nothing about ramp or filtering. Also MDFCs are ignored (they count as 0 mana spells).")
    print(" > IMPORTANT: Did you remember to set your User-Agent if you're using source code to run this?")

    while True:
        try:
            query()
        except (SkipException, MoxfieldError, RuntimeError, ConnectionError) as e:
            print(e)
            print(" > Query cleared. Skipping to the beginning.")
            continue
        except (ExitException, UserAgentError) as e:
            print(e)
            input("   Press enter to exit.")
            break


if __name__ == '__main__':
    main()
