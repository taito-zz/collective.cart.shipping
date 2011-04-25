#from Acquisition import aq_inner
from zope.app.component.hooks import getSite
from zope.component import adapts
from zope.interface import alsoProvides, implements
from OFS.interfaces import IItem
from collective.cart.core.interfaces import IPortal
from collective.cart.shipping.interfaces import(
    IShippingMethod,
    IShippingMethodAnnotations,
)


class ShippingMethodAdapter(object):

    adapts(IShippingMethodAnnotations)
    implements(IShippingMethod)

    def __init__(self, context):
        self.context = context

    def shipping_cost(self, weight, price):
#        context = aq_inner(self.context)
        base_charge = self.context.base_charge
        weight_charge = self.context.weight_charge
        fuel_rate = self.context.fuel_rate
        insurance_base = self.context.insurance_base
        insurance_rate = self.context.insurance_rate
        risk_rate = self.context.risk_rate
        cost = (base_charge + weight * weight_charge) \
            * (100 + fuel_rate) / 100 \
            * (100 + risk_rate) / 100 + insurance_base\
            + price * (insurance_rate) / 100
#        portal = getSite()
#        if not IItem.providedBy(portal):
#            alsoProvides(portal, IItem)
        return cost
#        return IPortal(portal).decimal_price(cost)
