from Acquisition import aq_inner
from zope.component import adapts, getMultiAdapter
from zope.interface import implements
from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.cart.core.interfaces import (
    IAvailableShippingMethods,
    IPortalSessionCatalog,
    IUpdateShippingMethod,
)
from collective.cart.shipping.content.shipping import ShippingMethodAnnotations
from collective.cart.shipping.interfaces import IShippingMethod

class AvailableShippingMethods(object):

    adapts(IItem)
    implements(IAvailableShippingMethods)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog(
            object_provides = IShippingMethod.__identifier__,
        )
        if len(brains) != 0:
            return brains

class UpdateShippingMethod(object):

    adapts(IItem)
    implements(IUpdateShippingMethod)

    def __init__(self, context):
        self.context = context

    def __call__(self, method=None):
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        cart = getMultiAdapter((portal, portal.session_data_manager, portal.portal_catalog), IPortalSessionCatalog).cart
        if method is not None:
            if getattr(method, 'Type', None) != u'Shipping Method':
                method = method[0]
            cart.shipping_method = ShippingMethodAnnotations(method)
