from collective.cart.shipping.interfaces import ICountries
from zope.component import getUtility
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


def CountryVocabularyFactory(context):
    items = [SimpleTerm(item[0], item[0], item[1]) for item in getUtility(ICountries).ordered_tuple_list()]
    return SimpleVocabulary(items)


directlyProvides(CountryVocabularyFactory, IVocabularyFactory)
