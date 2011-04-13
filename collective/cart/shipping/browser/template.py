from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ShippingMethodView(BrowserView):

    __call__ = ViewPageTemplateFile('templates/shipping_method.pt')
