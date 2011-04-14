from zope.component import adapts
from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from collective.cart.core.interfaces import IAvailableShippingMethods
from collective.cart.shipping.interfaces import IShippingMethod

class AvailableShippingMethods(object):

    adapts(IPloneSiteRoot)
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
