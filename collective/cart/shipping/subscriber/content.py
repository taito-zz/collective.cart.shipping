#from Acquisition import aq_inner, aq_parent
from persistent.dict import PersistentDict
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from Products.Archetypes.interfaces import IObjectInitializedEvent
from collective.cart.core.interfaces import (
    ICartContentType,
    ICartProduct,
    ICartProductContentType,
)

from collective.cart.shipping.content.shipping import ShippingMethodAnnotations
from collective.cart.shipping.interfaces import (
    IPortal,
    IProduct,
)

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
        weight_unit = iproduct.weight_unit,
        weight = iproduct.weight,
        dimension = iproduct.height * iproduct.width * iproduct.depth / 10 ** 6,
    )
    IAnnotations(context)['collective.cart.shipping'] = PersistentDict(items)

#@adapter(ICartFolderContentType, IObjectInitializedEvent)
#def delete_old_cart_folder(context, event):
#    """Delete Cart Folder in the same hierarchy."""
#    assert context == event.object
#    catalog = getToolByName(context, 'portal_catalog')
#    parent = aq_parent(aq_inner(context))
#    path = '/'.join(parent.getPhysicalPath())
#    brains = catalog(
#        object_provides=ICartFolderContentType.__identifier__,
#        path=dict(
#            query=path,
#            depth=1,
#        ),
#    )
#    objs = [brain.getObject() for brain in brains if brain.UID != context.UID()]
#    if objs:
#        for obj in objs:
#            obj.unindexObject()
#            del parent[obj.id]
#    ## Make the content language neutral
#    if context.getField('language').get(context) != '':
#        context.getField('language').set(context, '')

