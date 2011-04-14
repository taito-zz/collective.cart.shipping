try:
    import unittest2 as unittest
except ImportError:
    import unittest
#from zope.component import getUtility, getMultiAdapter
#from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from Products.CMFCore.utils import getToolByName
from collective.cart.shipping.tests.base import TestCase
#from AccessControl import getSecurityManager

class TestSetup(TestCase):

    def afterSetUp(self):
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')
        self.properties = getToolByName(self.portal, 'portal_properties')
        self.site_properties = getattr(self.properties, 'site_properties')
        self.navtree_properties = getattr(self.properties, 'navtree_properties')
#        self.controlpanel = getToolByName(self.portal, 'portal_controlpanel')
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.content_types = [
            'ShippingMethod',
        ]
        self.types = getToolByName(self.portal, 'portal_types')
        self.workflow = getToolByName(self.portal, 'portal_workflow')
#        self.actions = getToolByName(self.portal, 'portal_actions')
#        self.sm = getSecurityManager()
#        self.setRoles(('Manager',))

    def test_is_collective_cart_core_installed(self):
        self.failUnless(self.installer.isProductInstalled('collective.cart.core'))

    def test_is_collective_cart_shipping_installed(self):
        self.failUnless(self.installer.isProductInstalled('collective.cart.shipping'))

    ## Content Types
    def test_content_installed(self):
        for type in self.content_types:
            self.failUnless(type in self.types.objectIds())

    def test_shipping_method_content_type(self):
        item = self.types.getTypeInfo('ShippingMethod')
        self.assertEquals('Shipping Method', item.title)
        self.assertEquals('Shipping Method', item.description)
        self.assertEquals('ShippingMethod', item.content_meta_type)
        self.assertEquals('addShippingMethod', item.factory)
        self.assertEquals('view', item.immediate_view)
        self.assertEquals(True, item.global_allow)
        self.assertEquals(False, item.filter_content_types)
        self.assertEquals((), item.allowed_content_types)
        self.assertEquals('view', item.default_view)
        self.assertEquals(('view',), item.view_methods)
        aliases = {'edit': 'atct_edit', 'sharing': '@@sharing', '(Default)': '(dynamic view)', 'view': '(selected layout)'}
        self.assertEquals(aliases, item.getMethodAliases())
        actions = [
            (action.title, action.id, action.getActionExpression(), action.visible, action.permissions) for action in item.listActions()
        ]
        self.assertEquals(
            [
                ('View', 'view', 'string:${object_url}', True, (u'View',)),
                ('Edit', 'edit', 'string:${object_url}/edit', True, (u'Modify portal content',))
            ],
            [
                (action.title, action.id, action.getActionExpression(), action.visible, action.permissions) for action in item.listActions()
            ]
        )


    def test_typesLinkToFolderContentsInFC(self):
        self.failUnless('ShippingMethod' not in self.site_properties.getProperty('typesLinkToFolderContentsInFC'))

    ## navtree_properties
    def test_not_in_navtree(self):
        self.failUnless('ShippingMethod' in self.navtree_properties.getProperty('metaTypesNotToList'))

    ## catalog.xml
#    def test_catalog_index(self):
#        self.failUnless('uid' in self.catalog.indexes())

    def test_metadata(self):
        self.failUnless('from_country' in self.catalog.schema())
        self.failUnless('to_country' in self.catalog.schema())
        self.failUnless('base_charge' in self.catalog.schema())
        self.failUnless('weight_charge' in self.catalog.schema())
        self.failUnless('fuel_rate' in self.catalog.schema())
        self.failUnless('insurance_base' in self.catalog.schema())
        self.failUnless('insurance_rate' in self.catalog.schema())
        self.failUnless('risk_rate' in self.catalog.schema())
        self.failUnless('min_delivery_days' in self.catalog.schema())
        self.failUnless('max_delivery_days' in self.catalog.schema())
        self.failUnless('dimension_weight_ratio' in self.catalog.schema())

    ## worlflows.xml
    def test_cart_folder_workflow_chain(self):
        self.failUnless('simple_publication_workflow' in self.workflow.getChainForPortalType('ShippingMethod'))

#    def test_portlet(self):
#        left_column = getUtility(IPortletManager, name=u"plone.leftcolumn")
#        left_assignable = getMultiAdapter((self.portal, left_column), IPortletAssignmentMapping)
#        self.failUnless('cart' in left_assignable.keys())

    ## Uninstalling
    def test_uninstall(self):
        self.installer.uninstallProducts(['collective.cart.shipping'])
        self.failUnless(not self.installer.isProductInstalled('collective.cart.shipping'))
        for typ in self.content_types:
            self.failIf(typ in self.types.objectIds())

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
