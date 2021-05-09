
class LaunchpadError(Exception):
    """ Base error. """
    pass

class DeviceNotFound(LaunchpadError):
    """ Launchpad device could not be found. """
    pass

class InvalidCoordinate(LaunchpadError):
    """ Invalid coordinate was provided. """
    pass

class NoMacroBound(LaunchpadError):
    """ No macro is defined for the coordinate. """
    pass
