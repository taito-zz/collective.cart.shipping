from Acquisition import aq_inner
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from collective.cart.core.interfaces import (
    IAvailableShippingMethods,
    IPortalSessionCatalog,
    IUpdateShippingMethod,
)
from collective.cart.shipping.interfaces import (
    IShippingMethod,
)


class ShippingViewletBase(ViewletBase):

    @property
    def current_url(self):
        """Returns current url"""
        context_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_context_state')
        return context_state.current_page_url()


class ShippingMethodViewlet(ShippingViewletBase):

    index = render = ViewPageTemplateFile("viewlets/shipping_method.pt")

    def update(self):
        form = self.request.form
        if form.get('form.button.UpdateShippingMethod', None) is not None:
            uid = form.get('shipping_method')
            if uid != self.selected_shipping_method.uid:
                context = aq_inner(self.context)
                catalog = getToolByName(context, 'portal_catalog')
                brains = catalog(
                    UID = uid,
                    object_provides = IShippingMethod.__identifier__,
                )
                IUpdateShippingMethod(context)(brains)
                return self.request.response.redirect(self.current_url)

    @property
    def available_shipping_method(self):
        context = aq_inner(self.context)
        return IAvailableShippingMethods(context)()

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
        portal = getToolByName(context, 'portal_url').getPortalObject()
        sdm = getToolByName(context, 'session_data_manager')
        catalog = getToolByName(context, 'portal_catalog')
        cart = getMultiAdapter((portal, sdm, catalog), IPortalSessionCatalog).cart
        return cart.shipping_method
