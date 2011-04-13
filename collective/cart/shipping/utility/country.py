from zope.interface import implements
from pycountry import countries
from collective.cart.shipping.interfaces import (
    ICountries,
)

class Countries(object):

    implements(ICountries)

    def __call__(self):
        """Returns country_code : country_name dictionary."""
        data = dict([(country.alpha2, country.name) for country in countries.objects])
        return data

    def ordered_tuple_list(self):
        """Returns ordered tuple of code and name in a list."""
        data = [(item[1], item[0]) for item in self().items()]
        data.sort()
        data = [(item[1], item[0]) for item in data]
        return data
