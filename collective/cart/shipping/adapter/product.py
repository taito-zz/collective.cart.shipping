from zope.component import adapts
from zope.interface import implements
from collective.cart.core.adapter.cart import CartProductAdapter
from collective.cart.core.content import CartProduct
from collective.cart.core.interfaces import (
    ICartProduct,
    ICartProductAdapter,
#    IProductAnnotations,
#    IProductAnnotationsAdapter,
)


class CartProductAdapter(CartProductAdapter):
#class CartProductAdapter(object):

    adapts(CartProduct)
    implements(ICartProductAdapter)

    def __init__(self, context):
        self.context = context

    @property
    def dimension(self):
        height = self.context.height
        width = self.context.width
        depth = self.context.depth
        if height and width and depth:
            return float(height * width * depth) / 10 ** 6

    def weight_in_kg(self, method=None):
        weight = self.context.weight
        if self.context.weight_unit == 'g':
            weight = self.context.weight / 1000
        if self.dimension and method:
            ratio = method.dimension_weight_ratio
            d_weight = self.dimension * ratio
            if d_weight > weight:
                weight = d_weight
        return weight
