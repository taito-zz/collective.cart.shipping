from zope.interface import Interface


class IShippingMethodAdapter(Interface):

    def shipping_cost(weight, price):
        """Returns shipping cost."""
