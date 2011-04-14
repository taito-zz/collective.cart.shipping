try:
    import unittest2 as unittest
except ImportError:
    import unittest

from mock import Mock, patch

from zope.component import provideAdapter
from zope.interface import alsoProvides

from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from collective.cart.core.interfaces import IAvailableShippingMethods
from collective.cart.shipping.adapter.portal import AvailableShippingMethods


class Catalog(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)

    def __call__(self, **kwargs):
        return [Mock(), Mock()]

def gtbn(obj, name):
    return Catalog()

class MockTest(unittest.TestCase):

    def test_aaa(self):
        a = 'aaa'
        self.assertEqual('aaa', a)

    @patch('collective.cart.shipping.adapter.portal.getToolByName', gtbn)
    def test_adapter(self):
        provideAdapter(AvailableShippingMethods)
        portal = Mock()
        alsoProvides(portal, IPloneSiteRoot)
        asm = IAvailableShippingMethods(portal)
        self.assertEqual(2, len(asm()))

def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(MockTest),
    ])
