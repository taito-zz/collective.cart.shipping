from collective.cart.core.interfaces import ICart as ICoreCart
from collective.cart.core.interfaces import IPortal as ICorePortal
from collective.cart.core.interfaces import IUpdateCart
from collective.cart.shipping.interfaces import ICart
from collective.cart.shipping.interfaces import IPortal
from collective.cart.shipping.interfaces import IShippingMethod
from zope.component import adapter


@adapter(IUpdateCart)
def set_shipping_cost(event):
    cart = event.cart
    method = IPortal(cart).selected_shipping_method
    weight = ICart(cart).weight
    price = float(ICoreCart(cart).subtotal)
    cost = IShippingMethod(method).shipping_cost(weight, price)
    cost = ICorePortal(cart).decimal_price(cost)
    item = dict(shipping_cost=cost)
    cart.totals.update(item)
