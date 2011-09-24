from zope.interface import Attribute
from zope.interface import Interface


class IPortal(Interface):

    def available_shipping_method():
        """Returns list of availabel shipping method brain if else None."""

    def selected_shipping_method():
        """Retruns selected shpping method from cart."""

    def update_shipping_method(form):
        """Update shipping method."""


class IShippingMethod(Interface):

    def shipping_cost(weight, price):
        """Returns shipping cost."""


class IProduct(Interface):

    weight_unit = Attribute('Weight Unit')
    weight = Attribute('Weight')
    height = Attribute('Height')
    width = Attribute('Width')
    depth = Attribute('Depth')


class ICartProduct(Interface):

    def weight_in_kg(method):
        """Returns weight in kg."""


class ICart(Interface):

    def weight():
        """Returns weight."""
