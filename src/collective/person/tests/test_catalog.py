# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.person.content.person import IPerson

from collective.person.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']
        self.pc = self.portal['portal_personcatalog']
        self.indexes = self.pc.indexes()
        self.metadata = self.pc.schema()

    def test_index_fullname_setup(self):
        self.assertTrue('fullname' in self.indexes)

    def test_index_given_name_setup(self):
        self.assertTrue('given_name' in self.indexes)

    def test_index_surname_setup(self):
        self.assertTrue('surname' in self.indexes)

    def test_index_birthday_setup(self):
        self.assertTrue('birthday' in self.indexes)

    def test_index_cooked_birthday_setup(self):
        self.assertTrue('cooked_birthday' in self.indexes)

    def test_index_has_portrait_setup(self):
        self.assertTrue('has_portrait' in self.indexes)

    def test_metadata_fullname_setup(self):
        self.assertTrue('fullname' in self.metadata)

    def test_metadata_given_name_setup(self):
        self.assertTrue('given_name' in self.metadata)

    def test_metadata_surname_setup(self):
        self.assertTrue('surname' in self.metadata)

    def test_metadata_birthday_setup(self):
        self.assertTrue('birthday' in self.metadata)

    def test_metadata_has_portrait_setup(self):
        self.assertTrue('has_portrait' in self.metadata)

    def test_indexer_cooked_birthday(self):
        from datetime import date
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        p1.birthday = date(1969, 7, 21)
        p1.reindexObject()
        results = self.pc.searchResults(portal_type='collective.person.person',
                                        cooked_birthday='0721')
        self.assertEquals(len(results), 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
