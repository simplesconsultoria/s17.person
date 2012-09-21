# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import createObject
from zope.component import queryUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.app.referenceablebehavior.referenceable import IReferenceable
from plone.dexterity.interfaces import IDexterityFTI

from plone.dexterity.schema import SCHEMA_CACHE

from plone.uuid.interfaces import IAttributeUUID

from s17.person.content.person import IPerson

from s17.person.testing import INTEGRATION_TESTING


class IntegrationTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        # Invalidate schema cache
        SCHEMA_CACHE.invalidate('Person')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']

    def test_adding(self):
        self.folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(IPerson.providedBy(p1))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='Person')
        self.assertNotEquals(None, fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='Person')
        schema = fti.lookupSchema()
        self.assertEquals(IPerson, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='Person')
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IPerson.providedBy(new_object))

    def test_is_referenceable(self):
        self.folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(IReferenceable.providedBy(p1))
        self.assertTrue(IAttributeUUID.providedBy(p1))

    def test_title(self):
        self.folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        p1.given_name = 'James T.'
        p1.surname = 'Kirk'
        self.assertEquals(p1.Title(), 'James T. Kirk')
        self.assertEquals(p1.title, 'James T. Kirk')
        self.assertEquals(p1.fullname, 'James T. Kirk')

    def test_birthday_past(self):
        from datetime import date
        birthday = date(1969, 7, 21)
        # Validate returns None if it is ok
        self.assertTrue(not IPerson['birthday'].validate(birthday))

    def test_birthday_future(self):
        from datetime import date
        from zope.interface import Invalid
        birthday = date(2069, 7, 21)
        # Date is in the future
        self.assertRaises(Invalid, IPerson['birthday'].validate, birthday)
