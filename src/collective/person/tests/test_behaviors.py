# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.component import queryUtility

from zope.interface import Invalid

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.behavior.interfaces import IBehavior

from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI

from collective.person.behaviors.base import INameFromFullName
from collective.person.behaviors.user import INameFromUserName
from collective.person.behaviors.user import IPloneUser


from collective.person.testing import INTEGRATION_TESTING


class BaseTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        self.folder = self.portal['test-folder']


class INameFromFullNameTest(BaseTestCase):

    name = 'collective.person.behaviors.base.INameFromFullName'

    def setUp(self):
        BaseTestCase.setUp(self)

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.name)
        self.assertNotEquals(None, registration)

    def test_set_as_default_in_person(self):
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        behaviors = fti.behaviors
        self.assertTrue(self.name in behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(INameFromFullName.providedBy(p1))

    def test_provide_new_id(self):
        from zope.container.interfaces import INameChooser
        chooser = INameChooser(self.folder)
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        p1.given_name = u'Dražen'
        p1.surname = u'Petrović'
        self.assertEquals(chooser.chooseName(None, p1), 'drazen-petrovic')

    def test_provide_new_id_resolve_conflict(self):
        from zope.container.interfaces import INameChooser
        chooser = INameChooser(self.folder)
        # Create a person with the id that would be generated from
        # name
        self.folder.invokeFactory('collective.person.person',
                                  'drazen-petrovic')
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        p1.given_name = u'Dražen'
        p1.surname = u'Petrović'
        self.assertEquals(chooser.chooseName(None, p1),
                          'drazen-petrovic-1')


class IPloneUserTest(BaseTestCase):

    name = 'collective.person.behaviors.user.IPloneUser'

    def setUpUsers(self):
        ''' Create plone users '''
        rt = self.portal.portal_registration
        usernames = ['user1', 'user2', ]
        for username in usernames:
            properties = {'username': username,
                          'fullname': username,
                          'email': '%s@foo.bar' % username,
                         }
            rt.addMember(username, username, properties=properties)

    def setUp(self):
        behaviors = []
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        fti.behaviors = tuple(behaviors)
        BaseTestCase.setUp(self)
        self.setUpUsers()

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.name)
        self.assertNotEquals(None, registration)

    def test_set_in_person(self):
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        behaviors = fti.behaviors
        self.assertTrue(self.name in behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        plone_user = IPloneUser(p1)
        self.assertNotEquals(None, plone_user)

    def test_valid_username(self):
        class MockUser(object):
            user_name = ''
        data = MockUser()
        data.user_name = 'user1'
        try:
            IPloneUser.validateInvariants(data)
        except Invalid:
            self.fail()

    def test_invalid_username(self):
        class MockUser(object):
            user_name = ''
        # Create a person
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        plone_user = IPloneUser(user1)
        plone_user.user_name = 'user1'
        # Now we validate the username user1
        data = MockUser()
        data.user_name = 'user1'
        self.assertRaises(Invalid, IPloneUser.validateInvariants, data)

    def test_get_user(self):
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        adapter = IPloneUser(user1)
        adapter.user_name = 'user1'
        self.assertNotEquals(None, adapter.getUser())


class INameFromUserNameTest(BaseTestCase):

    name = 'collective.person.behaviors.user.INameFromUserName'

    def setUp(self):
        behaviors = []
        behaviors.append('collective.person.behaviors.user.IPloneUser')
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        fti.behaviors = tuple(behaviors)
        BaseTestCase.setUp(self)

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.name)
        self.assertNotEquals(None, registration)

    def test_set_as_default_in_person(self):
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        behaviors = fti.behaviors
        self.assertTrue(self.name in behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(INameFromUserName.providedBy(p1))

    def test_provide_new_id(self):
        from collective.person.behaviors.user import NameFromUserName
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        plone_user = IPloneUser(p1)
        plone_user.user_name = 'dpetrovic'
        self.assertEquals(NameFromUserName(plone_user).title, 'dpetrovic')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)