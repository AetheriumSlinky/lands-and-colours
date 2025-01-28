"""User Agent information. Point this to a source of your liking where your User Agent resides."""

# For the time being Moxfield has locked its API and you must request a unique User Agent for yourself.
# I'm personally using a text file stored elsewhere on my system.

with open("moxfield_ua.txt", "r") as ua:
    info = ua.read()

user_agent = info
