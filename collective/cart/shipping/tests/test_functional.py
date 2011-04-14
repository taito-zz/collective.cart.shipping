try:
    import unittest2 as unittest
except ImportError:
    import unittest
from doctest import ELLIPSIS, NORMALIZE_WHITESPACE, REPORT_ONLY_FIRST_FAILURE
from Testing import ZopeTestCase as ztc
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from collective.cart.core.content.product import ProductAnnotations
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IAddableToCart, IProduct
from collective.cart.shipping.tests import base


OF = REPORT_ONLY_FIRST_FAILURE | NORMALIZE_WHITESPACE | ELLIPSIS

class TestSetup(base.FunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
        wftool = getToolByName(self.portal, 'portal_workflow')
        self.portal.invokeFactory(
            'CartFolder',
            'cfolder',
        )
        cfolder = self.portal.cfolder
        cfolder.reindexObject()
        self.portal.invokeFactory(
            'Document',
            'doc01',
            title='Document01'
        )
        doc01 = self.portal.doc01
        wftool.doActionFor(doc01, "publish")
        doc01.reindexObject()
        alsoProvides(doc01, IAddableToCart)
        IAnnotations(doc01)['collective.cart.core'] = ProductAnnotations()
        product01 = IProduct(doc01)
        product01.price = 10.0
        product01.stock = 20
        product01.unlimited_stock = False
        product01.max_addable_quantity = 30

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/browser.txt',
            package='collective.cart.shipping',
            test_class=TestSetup,
            optionflags=OF),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
