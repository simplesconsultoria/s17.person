# -*- coding: utf-8 -*-
import unittest2 as unittest

from five import grok
from zope.component import queryUtility

from zope.interface import Invalid

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.behavior.interfaces import IBehavior

from plone.dexterity.fti import DexterityFTI
from plone.dexterity.interfaces import IDexterityFTI

from collective.person.content.person import Person
from collective.person.content.person import IPerson

from collective.person.behaviors.contact import IContactInfo

from collective.person.behaviors.user import INameFromUserName
from collective.person.behaviors.user import IPloneUser


from collective.person.testing import INTEGRATION_TESTING


class IPersonish(IPerson):
    ''' A specialization of IPerson '''


class Personish(Person):
    ''' '''
    grok.implements(IPersonish)


class IPloneUserTest(unittest.TestCase):

    name = 'collective.person.behaviors.user.IPloneUser'

    layer = INTEGRATION_TESTING

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
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        behaviors = []
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        fti.behaviors = tuple(behaviors)
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

    def test_edit_username(self):
        class MockUser(object):
            user_name = ''
            __context__ = None
        # Create a person
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        plone_user = IPloneUser(user1)
        plone_user.user_name = 'user1'
        user1.reindexObject()
        # Now we validate if using the same user_name **and** in the same
        # context we have a green light
        data = MockUser()
        data.user_name = 'user1'
        data.__context__ = user1
        # Now we validate the username user1
        try:
            IPloneUser.validateInvariants(data)
        except Invalid:
            self.fail()

    def test_get_user(self):
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        adapter = IPloneUser(user1)
        adapter.user_name = 'user1'
        self.assertNotEquals(None, adapter.getUser())


class INameFromUserNameTest(unittest.TestCase):

    name = 'collective.person.behaviors.user.INameFromUserName'

    layer = INTEGRATION_TESTING

    def setUpType(self):
        person_fti = DexterityFTI(
            'Personish',
            factory='Personish',
            global_allow=True,
            behaviors=(
                'collective.person.behaviors.user.IPloneUser',
                'collective.person.behaviors.user.INameFromUserName',
                ),
            schema='collective.person.tests.test_behaviors.IPersonish',
            klass='collective.person.tests.test_behaviors.Personish'
        )
        self.pt._setObject('Personish', person_fti)

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        self.setUpType()

    def test_registration(self):
        registration = queryUtility(IBehavior, name=self.name)
        self.assertNotEquals(None, registration)

    def test_set_as_default_in_person(self):
        fti = queryUtility(IDexterityFTI,
                           name='Personish')
        behaviors = fti.behaviors
        self.assertTrue(self.name in behaviors)

    def test_adapt_content(self):
        self.folder.invokeFactory('Personish', 'p1')
        p1 = self.folder['p1']
        self.assertTrue(INameFromUserName.providedBy(p1))

    def test_provide_new_id(self):
        from plone.app.content.interfaces import INameFromTitle
        self.folder.invokeFactory('Personish', 'p1')
        p1 = self.folder['p1']
        plone_user = IPloneUser(p1)
        plone_user.user_name = 'dpetrovic'
        self.assertEquals(INameFromTitle(p1).title, 'dpetrovic')


class MockContactInfo(object):
    emails = []
    instant_messengers = []
    telephones = []


class IContactInfoTest(unittest.TestCase):

    name = 'collective.person.behaviors.contact.IContactInfo'

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.pt = self.portal.portal_types
        self.pc = self.portal['portal_personcatalog']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']
        behaviors = []
        behaviors.append(self.name)
        fti = queryUtility(IDexterityFTI,
                           name='collective.person.person')
        fti.behaviors = tuple(behaviors)

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
        adapter = IContactInfo(p1)
        self.assertNotEquals(None, adapter)

    def test_emails(self):
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        adapter = IContactInfo(user1)
        adapter.emails = [{'category': 'work', 'data': 'foo@bar.com'},
                          {'category': 'home', 'data': 'bar@foo.com'}]
        self.assertEquals(len(adapter.emails), 2)

    def test_valid_emails(self):
        data = MockContactInfo()
        data.emails = [{'category': 'home',
                        'data': 'foo@bar.com'},
                       {'category': 'work',
                        'data': 'bar@foo.com'}]
        try:
            IContactInfo.validateInvariants(data)
        except Invalid:
            self.fail()

    def test_invalid_emails(self):
        data = MockContactInfo()
        # Wrong format
        data.emails = [{'category': 'home',
                        'data': 'ee.ee.br'}, ]
        self.assertRaises(Invalid, IContactInfo.validateInvariants, data)

    def test_instant_messengers(self):
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        adapter = IContactInfo(user1)
        adapter.instant_messengers = [{'category': 'gtalk',
                                       'data': 'foo@bar.com'},
                                      {'category': 'skype',
                                       'data': 'bar@foo.com'}]
        self.assertEquals(len(adapter.instant_messengers), 2)

    def test_telephones(self):
        self.folder.invokeFactory('collective.person.person', 'user1')
        user1 = self.folder['user1']
        adapter = IContactInfo(user1)
        adapter.telephones = [{'category': 'home',
                               'data': '+5511555.1213'},
                              {'category': 'work',
                               'data': '+5511316.9876'}]
        self.assertEquals(len(adapter.telephones), 2)

    def test_valid_telephones(self):
        data = MockContactInfo()
        data.telephones = [{'category': 'home',
                           'data': '+5511555.1213'},
                          {'category': 'work',
                           'data': '+5511316.9876'}]
        try:
            IContactInfo.validateInvariants(data)
        except Invalid:
            self.fail()

    def test_invalid_telephones(self):
        data = MockContactInfo()
        # No Country Code
        data.telephones = [{'category': 'home',
                           'data': '11555.1213'}, ]
        self.assertRaises(Invalid, IContactInfo.validateInvariants, data)

        data = MockContactInfo()
        # Letters, instead of numbers
        data.telephones = [{'category': 'home',
                            'data': '+5511555.SIMPLES'}, ]
        self.assertRaises(Invalid, IContactInfo.validateInvariants, data)

    def test_telephones_indexed(self):
        self.folder.invokeFactory('collective.person.person', 'p1')
        p1 = self.folder['p1']
        adapter = IContactInfo(p1)
        adapter.telephones = [{'category': 'home',
                               'data': '+5511555.1213'},
                              {'category': 'work',
                               'data': '+5511316.9876'}]
        p1.reindexObject()
        results = self.pc.searchResults(portal_type='collective.person.person',
                                        telephones='home:+5511555.1213')
        self.assertEquals(len(results), 1)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
