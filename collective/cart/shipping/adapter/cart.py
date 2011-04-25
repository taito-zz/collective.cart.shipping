from Acquisition import aq_inner
from zope.interface import implements
from zope.component import adapts#, getUtility#, getMultiAdapter
#from Products.ZCatalog.interfaces import IZCatalog
#from Products.CMFCore.utils import getToolByName
#from collective.cart.core.adapter.cart import CartItself
#from collective.cart.core.content import CartProduct
from collective.cart.core.interfaces import ICart as ICoreCart
from collective.cart.core.interfaces import (
#    ICart,
    ICartContentType,
#    ICartItself,
#    ICartAdapter,
#    ICartProduct,
#    ICartProductAdapter,
#    ICartProductOriginal,
#    IProduct,
#    IProductAnnotationsAdapter,
#    ISelectRange,
#    IShippingCost,
)
from collective.cart.shipping.interfaces import (
    ICart,
    ICartProduct,
    IPortal,
#    IShippingMethodAdapter,
)


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

#    @property
#    def shipping_cost(self):
#        method = self.context.shipping_method
#        if method is not None:
#            sma = IShippingMethodAdapter(method)
#            return sma.shipping_cost(self.weight, self.subtotal)
#        else:
#            return 0
