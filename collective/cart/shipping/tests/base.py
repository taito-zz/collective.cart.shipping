try:
    from Zope2.App import zcml
except ImportError:
    from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():

    fiveconfigure.debug_mode = True
    import collective.cart
    zcml.load_config('configure.zcml', collective.cart.shipping)

    fiveconfigure.debug_mode = False

    ztc.installPackage('collective.cart.shipping')

setup_product()
ptc.setupPloneSite(products=['collective.cart.shipping',])

class TestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If
    necessary, we can put common utility or setup code in here. This
    applies to unit test cases.
    """


class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use
    doctest syntax. Again, we can put basic common utility or setup
    code in here.
    """