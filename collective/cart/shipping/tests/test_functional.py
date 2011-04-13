try:
    import unittest2 as unittest
except ImportError:
    import unittest
from doctest import ELLIPSIS, NORMALIZE_WHITESPACE, REPORT_ONLY_FIRST_FAILURE
from Testing import ZopeTestCase as ztc
from collective.cart.shipping.tests import base

OF = REPORT_ONLY_FIRST_FAILURE | NORMALIZE_WHITESPACE | ELLIPSIS

class TestSetup(base.FunctionalTestCase):

    def afterSetUp( self ):
        """After SetUp"""
        self.setRoles(('Manager',))
        ## Set up sessioning objects
        ztc.utils.setupCoreSessions(self.app)
#        self.portal.invokeFactory(
#            'Document',
#            'document01',
#            title='Document01'
#        )
#        document01 = self.portal.document01
#        document01.reindexObject()

def test_suite():
    return unittest.TestSuite([

        ztc.FunctionalDocFileSuite(
            'tests/functional/browser.txt',
            package='collective.cart.shipping',
            test_class=TestSetup,
            optionflags=OF),

            ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
