from Testing import ZopeTestCase as ztc
from collective.cart.core.content.product import ProductAnnotations
from collective.cart.core.interfaces import IAddableToCart, IProduct
from collective.cart.shipping.tests.base import FUNCTIONAL_TESTING
from decimal import Decimal
from hexagonit.testing.browser import Browser
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.testing import layered
from zope.annotation.interfaces import IAnnotations
from zope.interface import alsoProvides
from zope.testing import renormalizing

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest2 as unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    # Update global variables within the tests.
    self.globs.update({
        'portal': layer['portal'],
        'portal_url': layer['portal'].absolute_url(),
        'browser': Browser(layer['app']),
    })
    ztc.utils.setupCoreSessions(layer['app'])
    portal = self.globs['portal']
    browser = self.globs['browser']
    portal_url = self.globs['portal_url']
    browser.setBaseUrl(portal_url)

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    portal.invokeFactory(
        'CartFolder',
        'cfolder',
    )
    cfolder = portal.cfolder
    cfolder.reindexObject()
    portal.invokeFactory(
        'Document',
        'doc01',
        title='Document01'
    )
    doc01 = portal.doc01
    doc01.reindexObject()
    self.globs['doc01_url'] = doc01.absolute_url()
    self.globs['cart_url'] = '{0}/@@cart'.format(portal_url)
    alsoProvides(doc01, IAddableToCart)
    IAnnotations(doc01)['collective.cart.core'] = ProductAnnotations()
    product01 = IProduct(doc01)
    product01.price = Decimal('10.00')
    product01.stock = 20
    product01.unlimited_stock = False
    product01.max_addable_quantity = 30

    transaction.commit()


def tearDown(self):
    portal = self.globs['portal']
    del portal['doc01']
    del portal['cfolder']
    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, tearDown=tearDown, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, tearDown=tearDown, globs=dict(layer=layer)),
        layer=layer)


def test_suite():
    return unittest.TestSuite([
        DocFileSuite('functional/browser.txt'),
        ])
