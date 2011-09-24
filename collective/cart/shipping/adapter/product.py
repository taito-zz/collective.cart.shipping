from Acquisition import aq_inner
from collective.cart.core.interfaces import IAddableToCart
from collective.cart.core.interfaces import ICartProductContentType
from collective.cart.shipping.content.product import ProductAnnotations
from collective.cart.shipping.interfaces import ICartProduct
from collective.cart.shipping.interfaces import IProduct
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements


class Product(object):

    adapts(IAddableToCart)
    implements(IProduct)

    def __init__(self, context):
        self.context = context

    def __getattr__(self, attr):
        if attr == 'context':
            return self.context
        else:
            annotations = IAnnotations(self.context)
            if annotations.get('collective.cart.shipping', None) is None:
                annotations['collective.cart.shipping'] = ProductAnnotations()
            return getattr(annotations['collective.cart.shipping'], attr)

    def __setattr__(self, attr, value):
        if attr == 'context':
            self.__dict__[attr] = value
        else:
            annotations = IAnnotations(self.context)
            setattr(annotations['collective.cart.shipping'], attr, value)


class CartProductAdapter(object):

    adapts(ICartProductContentType)
    implements(ICartProduct)

    def __init__(self, context):
        self.context = context

#    @property
#    def dimension(self):
#        height = self.context.height
#        width = self.context.width
#        depth = self.context.depth
#        if height and width and depth:
#            return float(height * width * depth) / 10 ** 6

    def weight_in_kg(self, method=None):
        context = aq_inner(self.context)
        info = IAnnotations(context)['collective.cart.shipping']
        weight = info['weight']
        dimension = info['dimension']
        if info['weight_unit'] == 'g':
            weight = weight / 1000
        if dimension != 0 and method:
            ratio = method.dimension_weight_ratio
            d_weight = dimension * ratio
            if d_weight > weight:
                weight = d_weight
        return weight
