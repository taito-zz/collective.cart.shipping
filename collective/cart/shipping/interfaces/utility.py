from zope.interface import Interface


class ICountries(Interface):

    def __call__():
        """Returns country_code : country_name dictionary."""

    def ordered_tuple_list():
        """Returns ordered tuple of code and name in a list."""
