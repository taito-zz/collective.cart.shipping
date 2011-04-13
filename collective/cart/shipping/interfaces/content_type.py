from zope.interface import Interface
from zope import schema
from collective.cart.shipping import CartShippingMessageFactory as _


class IShippingMethod(Interface):

    from_country = schema.Choice(
        title=_(u"Country From"),
        required=False,
        description=_(u"Select countries from which this shipping method is applied."),
        vocabulary=_(u"Countries"),
    )

    to_country = schema.Choice(
        title=_(u"Country To"),
        required=False,
        description=_(u"Select countries to which this shipping method is applied."),
        vocabulary=_(u"Countries"),
    )

    base_charge = schema.Float(
        title=_(u"Base Shipping Charge"),
        description=_(u"This is starting charge for this shipping method."),
        required=True,
        default=0.0,
   )

    weight_charge = schema.Float(
        title=_(u"Weight Charge"),
        description=_(u"This charge will be added every kg of weight linearly."),
        required=True,
        default=0.0,
   )

    fuel_rate = schema.Float(
        title=_(u"Fuel Rate"),
        description=_(u"Fuel Rate usually changes every month."),
        required=True,
        default=0.0,
   )

    insurance_base = schema.Float(
        title=_(u"Insurance Base Charge"),
        description=_(u""),
        required=True,
        default=0.0,
   )

    insurance_rate = schema.Float(
        title=_(u"Insurance Rate"),
        description=_(u"This rate will be added to the total product price."),
        required=True,
        default=0.0,
   )

    risk_rate = schema.Float(
        title=_(u"Risk Rate"),
        description=_(u""),
        required=True,
        default=0.0,
   )

    min_delivery_days = schema.Int(
        title=_(u"Minimum Delivery Days"),
        required=True,
   )

    max_delivery_days = schema.Int(
        title=_(u"Maximum Delivery Days"),
        required=True,
   )

    dimension_weight_ratio = schema.Float(
        title=_(u"Dimention Weight Ratio"),
        description=_(u"1 m3 = ??? kg"),
        required=False,
   )

#    def country_code_name_tuples():
#        """Returns tuple of tuples for country code and name."""
