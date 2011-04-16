try:
    import unittest2 as unittest
except ImportError:
    import unittest

from mock import Mock, patch

from zope.component import provideAdapter
from zope.interface import alsoProvides

from OFS.interfaces import IItem
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from collective.cart.core.interfaces import IAvailableShippingMethods, IUpdateShippingMethod
from collective.cart.shipping.adapter.portal import AvailableShippingMethods, UpdateShippingMethod


class Catalog(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)

    def __call__(self, **kwargs):
        return [Mock(), Mock()]

class Url(object):

    def __init__(self, **kwargs):
        for k, v in kwargs.items(): setattr(self, k, v)

    def getPortalObject(self):
        return Mock()


def get_catalog(obj, name):
    return Catalog()

def get_url(obj, name):
    return Url()

class MockTest(unittest.TestCase):

    def test_aaa(self):
        a = 'aaa'
        self.assertEqual('aaa', a)

    @patch('collective.cart.shipping.adapter.portal.getToolByName', get_catalog)
    def test_available_shipping_methods(self):
        provideAdapter(AvailableShippingMethods)
        portal = Mock()
        alsoProvides(portal, IItem)
        asm = IAvailableShippingMethods(portal)
        self.assertEqual(2, len(asm()))

    
    @patch('collective.cart.shipping.adapter.portal.getMultiAdapter', Mock())
    @patch('collective.cart.shipping.adapter.portal.getToolByName', Mock())
    def test_update_shipping_method(self):
        provideAdapter(UpdateShippingMethod)
        context = Mock()
        alsoProvides(context, IItem)
        usm = IUpdateShippingMethod(context)
        self.assertEqual(None, usm())
#        method = Mock()
#        method.Type = Mock(return_value) = 'LazyMap'
#        import pdb; pdb.set_trace()
#        pass


def test_suite():
    return unittest.TestSuite([
        unittest.makeSuite(MockTest),
    ])
