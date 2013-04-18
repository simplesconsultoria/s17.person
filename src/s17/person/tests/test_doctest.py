#-*- coding: utf-8 -*-

from plone.testing import layered
from s17.person.testing import FUNCTIONAL_TESTING

import doctest
import unittest2 as unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(
            'tests/owner_edit.txt',
            package='s17.person'),
            layer=FUNCTIONAL_TESTING,),
    ])
    return suite
