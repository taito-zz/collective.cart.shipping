from zope.component import adapts
from zope.interface import implements
from collective.cart.shipping.interfaces import(
#    IShippingMethod,
    IShippingMethodAdapter,
    IShippingMethodAnnotations,
)


class ShippingMethodAdapter(object):

#    adapts(IShippingMethod)
    adapts(IShippingMethodAnnotations)
    implements(IShippingMethodAdapter)

    def __init__(self, context):
        self.context = context

    def shipping_cost(self, weight, price):
        base_charge = self.context.base_charge
        weight_charge = self.context.weight_charge
        fuel_rate = self.context.fuel_rate
        insurance_base = self.context.insurance_base
        insurance_rate = self.context.insurance_rate
        risk_rate = self.context.risk_rate
        return (base_charge + weight * weight_charge) \
            * (100 + fuel_rate) / 100 \
            * (100 + risk_rate) / 100 + insurance_base\
            + price * (insurance_rate) / 100
