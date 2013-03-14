# -*- coding: utf-8 -*-
import os
import unittest2 as unittest
from plone.namedfile.file import NamedBlobImage
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
        self.setup_content(self.folder)

    def setup_content(self, folder):
        path = os.path.dirname(__file__)
        data = open(os.path.join(path, 'picture.jpg')).read()
        image = NamedBlobImage(data, 'image/jpeg', u'picture.jpg')
        folder.invokeFactory('Person', 'p1')
        p1 = self.folder['p1']
        p1.picture = image
        self.p1 = p1

    def test_adding(self):
        self.assertTrue(IPerson.providedBy(self.p1))

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
        p1 = self.p1
        self.assertTrue(IReferenceable.providedBy(p1))
        self.assertTrue(IAttributeUUID.providedBy(p1))

    def test_title(self):
        p1 = self.p1
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

    def test_image_thumb(self):
        ''' Test if traversing to image_thumb returns an image
        '''
        p1 = self.p1
        self.assertTrue(p1.restrictedTraverse('image_thumb')().read())

    def test_image_tag(self):
        ''' Test if tag method works as expected
        '''
        p1 = self.p1
        expected = u'<img src="http://nohost/plone/test-folder/p1/@@images/'
        self.assertTrue(p1.tag().startswith(expected))

        expected = u'height="128" width="110" class="tileImage" />'
        self.assertTrue(p1.tag().endswith(expected))
