#-*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.person.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/owner_edit.txt',
                                     package='collective.person'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite