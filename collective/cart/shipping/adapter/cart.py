from Acquisition import aq_inner
from collective.cart.core.interfaces import ICart as ICoreCart
from collective.cart.core.interfaces import ICartContentType
from collective.cart.shipping.interfaces import ICart
from collective.cart.shipping.interfaces import ICartProduct
from collective.cart.shipping.interfaces import IPortal
from zope.component import adapts
from zope.interface import implements


class CartAdapter(object):

    adapts(ICartContentType)
    implements(ICart)

    def __init__(self, context):
        self.context = context

    @property
    def weight(self):
        context = aq_inner(self.context)
        products = ICoreCart(context).products
        method = IPortal(context).selected_shipping_method
        weights = [
            ICartProduct(product).weight_in_kg(method) for product in products
        ]
        return sum(weights)
