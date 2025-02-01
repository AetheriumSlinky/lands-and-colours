"""Exceptions classes."""

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


class MoxfieldError(Exception):
    """
    Used to raise Moxfield related errors.
    """
    pass

class UserAgentError(Exception):
    """
    Used to raise an error if your user-agent isn't valid.
    """
    pass
