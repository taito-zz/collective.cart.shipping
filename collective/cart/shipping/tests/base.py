from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import unittest2 as unittest


class CollectiveCartShippingLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        import collective.cart.core
        self.loadZCML(package=collective.cart.core)
        z2.installProduct(app, 'collective.cart.core')
        import collective.cart.shipping
        self.loadZCML(package=collective.cart.shipping)
        z2.installProduct(app, 'collective.cart.shipping')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.cart.core:default')
        self.applyProfile(portal, 'collective.cart.shipping:default')

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'collective.cart.core')
        z2.uninstallProduct(app, 'collective.cart.shipping')


FIXTURE = CollectiveCartShippingLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="CollectiveCartShippingLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="CollectiveCartShippingLayer:Functional")
CART_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="CollectiveCartShippingLayer:Integration")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING
