from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.Archetypes.public import ATFieldProperty
from Products.Archetypes.public import AnnotationStorage
from Products.Archetypes.public import DecimalWidget
from Products.Archetypes.public import FloatField
from Products.Archetypes.public import IntegerField
from Products.Archetypes.public import IntegerWidget
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import MultiSelectionWidget
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from collective.cart.shipping import PROJECTNAME
from collective.cart.shipping import _
from collective.cart.shipping.interfaces import IShippingMethodAnnotations
from collective.cart.shipping.interfaces import IShippingMethodContentType
from persistent import Persistent
from zope.interface import implements


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
        vocabulary_factory="collective.cart.shipping.countries",
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
        vocabulary_factory="collective.cart.shipping.countries",
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
        default=0.0,
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
        default=0.0,
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
        default=0.0,
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
        default=0.0,
    ),

   IntegerField(
        name='min_delivery_days',
        required=True,
        searchable=False,
        languageIndependent=True,
        storage=AnnotationStorage(),
        widget=IntegerWidget(
            label=_(u'Minimum Delivery Days'),
            size='2',
            maxlength='2',
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
            size='2',
            maxlength='2',
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
        default=250.0,
    ),

),
)

finalizeATCTSchema(ShippingMethodSchema, folderish=False, moveDiscussion=False)


class ShippingMethod(ATCTContent):

    implements(IShippingMethodContentType)

    portal_type = "ShippingMethod"
    _at_rename_after_creation = True

    schema = ShippingMethodSchema

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

registerType(ShippingMethod, PROJECTNAME)


class ShippingMethodAnnotations(Persistent):

    implements(IShippingMethodAnnotations)

    def __init__(self, brain):
        self.uid = brain.UID
        self.title = brain.Title
        self.description = brain.Description
        self.from_country = brain.from_country
        self.to_country = brain.to_country
        self.base_charge = brain.base_charge
        self.weight_charge = brain.weight_charge
        self.fuel_rate = brain.fuel_rate
        self.insurance_base = brain.insurance_base
        self.insurance_rate = brain.insurance_rate
        self.risk_rate = brain.risk_rate
        self.min_delivery_days = brain.min_delivery_days
        self.max_delivery_days = brain.max_delivery_days
        self.dimension_weight_ratio = brain.dimension_weight_ratio
