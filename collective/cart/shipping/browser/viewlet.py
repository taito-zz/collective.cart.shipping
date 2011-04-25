from Acquisition import aq_inner
from zope.component import getMultiAdapter, getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
#from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import (
    IRegularExpression,
#    IAvailableShippingMethods,
#    IPortalSessionCatalog,
#    IUpdateShippingMethod,
)
from collective.cart.core.browser.viewlet import CartTotalsProductsViewlet
from collective.cart.shipping import ShippingMethodMessageFactory as _
from collective.cart.shipping.interfaces import (
    IPortal,
    IProduct,
#    IShippingMethodContentType,
)


class ShippingViewletBase(ViewletBase):

    @property
    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_context_state')
        return context_state.current_page_url()


class EditProductViewlet(ShippingViewletBase):

    index = render = ViewPageTemplateFile("viewlets/edit_product.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdateProductShipping', None) is not None:
            context = aq_inner(self.context)
            product = IProduct(context)
            re = getUtility(IRegularExpression)
            fields = ['weight', 'height', 'width', 'depth']
            for field in fields:
                value = form.get(field)
                if re.float(value):
                    setattr(product, field, float(value))
            product.weight_unit = form.get('weight_unit')
            return self.request.response.redirect(self.current_url)


    def fields(self):
        context = aq_inner(self.context)
        product = IProduct(context)
        res = []
        weight_unit = dict(
            label = _(u'Weight Unit'),
            description = _('Select Weight Unit.'),
            field = self.select_weight_unit(product),
        )
        res.append(weight_unit)
        weight =dict(
            label = _('Weight'),
            description = _('Input Weight.'),
            field = '<input type="text" name="weight" id="weight" value="%s" size="5" />' % product.weight,
        )
        res.append(weight)
        height =dict(
            label = _('Height'),
            description = _('Input Height in cm unit.'),
            field = '<input type="text" name="height" id="height" value="%s" size="5" />' % product.height,
        )
        res.append(height)
        width = dict(
            label = _('Width'),
            description = _('Input Width in cm unit.'),
            field = '<input type="text" name="width" id="width" value="%s" size="5" />' % product.width,
        )
        res.append(width)
        depth = dict(
            label = _('Depth'),
            description = _('Input Depth in cm unit.'),
            field = '<input type="text" name="depth" id="depth" value="%s" size="5" />' % product.depth,
        )
        res.append(depth)
        return res

    def select_weight_unit(self, product):
        html = '<select name="weight_unit" id="weight_unit">'
        keys = ['g', 'kg']
        for key in keys:
            if product.weight_unit == key:
                html += '<option value="%s" selected="selected">%s</option>' % (key, key)
            else:
                html += '<option value="%s">%s</option>' % (key, key)
        html += '</select>'
        return html


class ShippingMethodViewlet(ShippingViewletBase):

    index = render = ViewPageTemplateFile("viewlets/shipping_method.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdateShippingMethod', None) is not None:
            context = aq_inner(self.context)
            IPortal(context).update_shipping_method(form)
            return self.request.response.redirect(self.current_url)

    @property
    def available_shipping_method(self):
        context = aq_inner(self.context)
        return IPortal(context).available_shipping_method

    @property
    def only_one_shipping_method(self):
        if len(self.available_shipping_method) == 1:
            return self.available_shipping_method[0]

    def shipping_method(self):
        if self.only_one_shipping_method:
            return self.only_one_shipping_method.Title
        selected = self.selected_shipping_method
        html = '<select name="shipping_method" id="shipping_method">'
        for method in self.available_shipping_method:
            if selected.uid == method.UID:
                html += '<option value="%s" selected="selected">%s</option>' % (selected.uid, selected.title)
            else:
                html += '<option value="%s">%s</option>' % (method.UID, method.Title)
        html += '</select>'
        return html

    @property
    def selected_shipping_method(self):
        context = aq_inner(self.context)
        return IPortal(context).selected_shipping_method


class ShippingCostViewlet(CartTotalsProductsViewlet):

    def label(self):
        return _(u'Shipping Cost')

    def total(self):
        context = aq_inner(self.context)
        return IPortal(context).cart.totals['shipping_cost']
