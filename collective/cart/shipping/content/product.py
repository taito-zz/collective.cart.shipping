from persistent import Persistent
from zope.interface import implements
from collective.cart.shipping.interfaces import IProductAnnotations

class ProductAnnotations(Persistent):
    implements(IProductAnnotations)
    def __init__(
        self,
        weight_unit = 'g',
        weight = 0,
        height = 0,
        width = 0,
        depth = 0,
        **kwargs
    ):
        self.weight_unit = weight_unit
        self.weight = weight
        self.height = height
        self.width = width
        self.depth = depth
