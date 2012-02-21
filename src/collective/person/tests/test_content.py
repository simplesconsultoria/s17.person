# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI
from plone.uuid.interfaces import IAttributeUUID

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

    def test_adding(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(IPerson.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='collective.person.person')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='collective.person.person')
        schema = fti.lookupSchema()
        self.assertEquals(IPerson, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='collective.person.person')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPerson.providedBy(new_object))

    def test_is_referenceable(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(IReferenceable.providedBy(p1))
        self.assertTrue(IAttributeUUID.providedBy(p1))

    def test_title(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        p1.given_name = 'James T.'
        p1.surname = 'Kirk'
        self.assertEquals(p1.Title(), 'James T. Kirk')
        self.assertEquals(p1.title, 'James T. Kirk')
        self.assertEquals(p1.fullname, 'James T. Kirk')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
