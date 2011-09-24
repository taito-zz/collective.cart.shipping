from Acquisition import aq_inner
from OFS.interfaces import IItem
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import IPortal as ICorePortal
from collective.cart.shipping.content.shipping import ShippingMethodAnnotations
from collective.cart.shipping.interfaces import IPortal
from collective.cart.shipping.interfaces import IShippingMethodContentType
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements


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
            object_provides=IShippingMethodContentType.__identifier__,
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
            brains = self.catalog(
                UID=uid,
                object_provides=IShippingMethodContentType.__identifier__,
            )
            if brains:
                method = brains[0]
                IAnnotations(
                    self.cart
                )[
                    'collective.cart.shipping.method'
                ] = ShippingMethodAnnotations(method)
