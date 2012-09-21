# -*- coding: utf-8 -*-
import doctest
import collective.person.utils


def test_suite():
    return doctest.DocTestSuite(collective.person.utils)
