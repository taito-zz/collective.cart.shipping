from zope.interface import implements
from zope.component import getUtility
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import (
    finalizeATCTSchema,
    ATContentTypeSchema
)
from collective.cart.shipping.interfaces import (
    IShippingMethod,
    ICountries,
)
from collective.cart.shipping import PROJECTNAME
from collective.cart.shipping import CartShippingMessageFactory as _
from Products.Archetypes.public import (
    AnnotationStorage,
    ATFieldProperty,
    registerType,
    Schema,
    FloatField,
    IntegerField,
    LinesField,
    DecimalWidget,
    IntegerWidget,
    MultiSelectionWidget,
)

ShippingMethodSchema = ATContentTypeSchema.copy() + Schema((

    LinesField(
        name='from_country',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=MultiSelectionWidget(
            label=_(u'From Country'),
            description=_(u'Select countries from which this shipping method is applied.'),
            size='15',
        ),
        vocabulary='country_code_name_tuples',
        enforceVocabulary=True,
    ),

    LinesField(
        name='to_country',
        required=False,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=MultiSelectionWidget(
            label=_(u'To Country'),
            description=_(u'Select countries to which this shipping method is applied.'),
            size='15',
        ),
        vocabulary='country_code_name_tuples',
        enforceVocabulary=True,
    ),

   FloatField(
       name='base_charge',
       required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            description=_(u'This is starting charge for this shipping method.'),
            label=_(u'Base Shipping Charge'),
        ),
        default=0.0,
    ),

   FloatField(
       name='weight_charge',
       required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            description=_(u'This charge will be added every kg of weight linearly.'),
            label=_(u'Weight Charge'),
        ),
        default=0.0,
    ),

   FloatField(
       name='fuel_rate',
       required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            description=_(u'Fuel Rate usually changes every month.'),
            label=_(u'Fuel Rate'),
        ),
        default = 0.0,
    ),


   FloatField(
        name='insurance_base',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Insurance Base Charge'),
            description=_(u''),
        ),
        default = 0.0,
    ),

   FloatField(
        name='insurance_rate',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Insurance Rate'),
            description=_(u'This rate will be added to the total product price.'),
        ),
        default = 0.0,
    ),


   FloatField(
        name='risk_rate',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            description=_(u''),
            label=_(u'Risk Rate'),
        ),
        default = 0.0,
    ),

   IntegerField(
        name='min_delivery_days',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=IntegerWidget(
            label=_(u'Minimum Delivery Days'),
            size = '2',
            maxlength = '2',
        ),
    ),

   IntegerField(
        name='max_delivery_days',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=IntegerWidget(
            label=_(u'Maximum Delivery Days'),
            size = '2',
            maxlength = '2',
        ),
    ),

   FloatField(
        name='dimension_weight_ratio',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=DecimalWidget(
            label=_(u'Dimention Weight Ratio'),
            description=_(u'1 m3 = ??? kg'),
        ),
        default = 250.0,
    ),

),
)

finalizeATCTSchema(ShippingMethodSchema, folderish=False, moveDiscussion=False)

class ShippingMethod(ATCTContent):

    implements(IShippingMethod)

    portal_type = "ShippingMethod"
    _at_rename_after_creation = True

    schema = ShippingMethodSchema

    title = ATFieldProperty('title')
    description = ATFieldProperty('description')
    from_country = ATFieldProperty('from_country')
    to_country = ATFieldProperty('to_country')
    base_charge = ATFieldProperty('base_charge')
    weight_charge = ATFieldProperty('weight_charge')
    fuel_rate = ATFieldProperty('fuel_rate')
    insurance_base = ATFieldProperty('insurance_base')
    insurance_rate = ATFieldProperty('insurance_rate')
    risk_rate = ATFieldProperty('risk_rate')
    min_delivery_days = ATFieldProperty('min_delivery_days')
    max_delivery_days = ATFieldProperty('max_delivery_days')
    dimension_weight_ratio = ATFieldProperty('dimension_weight_ratio')

    @property
    def country_code_name_tuples(self):
        """Returns tuple of tuples for country code and name."""
        return getUtility(ICountries).ordered_tuple_list()

registerType(ShippingMethod, PROJECTNAME)
