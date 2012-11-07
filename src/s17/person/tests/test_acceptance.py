import unittest

import robotsuite

from plone.testing import layered

from s17.person.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_persons.txt"),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
