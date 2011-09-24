from Products.Archetypes.interfaces import IObjectInitializedEvent
from collective.cart.core.interfaces import ICartContentType
from collective.cart.core.interfaces import ICartProduct
from collective.cart.core.interfaces import ICartProductContentType
from collective.cart.shipping.content.shipping import ShippingMethodAnnotations
from collective.cart.shipping.interfaces import IPortal
from collective.cart.shipping.interfaces import IProduct
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter


@adapter(ICartContentType, IObjectInitializedEvent)
def add_shipping_method(context, event):
    assert context == event.object
    if IAnnotations(context).get('collective.cart.shipping.method'):
        return
    method = IPortal(context).available_shipping_method[0]
    IAnnotations(context)['collective.cart.shipping.method'] = ShippingMethodAnnotations(method)


@adapter(ICartProductContentType, IObjectInitializedEvent)
def add_shipping_info(context, event):
    assert context == event.object
    product = ICartProduct(context).product
    iproduct = IProduct(product.context)
    items = dict(
        weight_unit=iproduct.weight_unit,
        weight=iproduct.weight,
        dimension=iproduct.height * iproduct.width * iproduct.depth / 10 ** 6,
    )
    IAnnotations(context)['collective.cart.shipping'] = PersistentDict(items)
