# -*- coding: utf-8 -*-

import unittest2 as unittest

from s17.person.testing import INTEGRATION_TESTING


class PermissionsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_add_permissions(self):
        permission = 's17.person: Add person'
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        self.assertListEqual(roles, expected)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
