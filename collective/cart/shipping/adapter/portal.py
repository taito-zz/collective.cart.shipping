from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements
from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IPortal as ICorePortal
from collective.cart.shipping.content.shipping import ShippingMethodAnnotations
from collective.cart.shipping.interfaces import (
    IPortal,
    IShippingMethodContentType,
)


class Portal(object):

    adapts(IItem)
    implements(IPortal)

    def __init__(self, context):
        self.context = context
        self.catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        self.cart = ICorePortal(aq_inner(self.context)).cart

    @property
    def available_shipping_method(self):
        brains = self.catalog(
            object_provides = IShippingMethodContentType.__identifier__,
        )
        if brains:
            return brains

    @property
    def selected_shipping_method(self):
        if self.cart:
            return IAnnotations(self.cart)['collective.cart.shipping.method']

    def update_shipping_method(self, form):
        uid = form.get('shipping_method')
        if uid != self.selected_shipping_method.uid:
#            context = aq_inner(self.context)
#            catalog = getToolByName(context, 'portal_catalog')
            brains = self.catalog(
                UID = uid,
                object_provides = IShippingMethodContentType.__identifier__,
            )
#            context = aq_inner(self.context)
#            portal = getToolByName(context, 'portal_url').getPortalObject()
#            cart = getMultiAdapter((portal, portal.session_data_manager, portal.portal_catalog), IPortalSessionCatalog).cart
            if brains:
                method = brains[0]
                IAnnotations(self.cart)['collective.cart.shipping.method'] = ShippingMethodAnnotations(method)
#            if method is not None:
#                if getattr(method, 'Type', None) != u'Shipping Method':
#                    method = method[0]
#                cart.shipping_method = ShippingMethodAnnotations(method)
#            IUpdateShippingMethod(context)(brains)

#class AvailableShippingMethods(object):

#    adapts(IItem)
#    implements(IAvailableShippingMethods)

#    def __init__(self, context):
#        self.context = context

#    @property
#    def available_shipping_method(self):
#        catalog = getToolByName(self.context, 'portal_catalog')
#        brains = catalog(
#            object_provides = IShippingMethod.__identifier__,
#        )
#        if len(brains) != 0:
#            return brains

#class UpdateShippingMethod(object):

#    adapts(IItem)
#    implements(IUpdateShippingMethod)

#    def __init__(self, context):
#        self.context = context

#    def __call__(self, method=None):
#        context = aq_inner(self.context)
#        portal = getToolByName(context, 'portal_url').getPortalObject()
#        cart = getMultiAdapter((portal, portal.session_data_manager, portal.portal_catalog), IPortalSessionCatalog).cart
#        if method is not None:
#            if getattr(method, 'Type', None) != u'Shipping Method':
#                method = method[0]
#            cart.shipping_method = ShippingMethodAnnotations(method)
