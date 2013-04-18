# -*- coding: utf-8 -*-
import logging

import os

from datetime import datetime

from zope.component import queryUtility

from plone.namedfile import NamedImage
from plone.namedfile.tests.base import getFile

from plone.dexterity.interfaces import IDexterityFTI

from Products.CMFCore.utils import getToolByName

from Products.GenericSetup.upgrade import listUpgradeSteps

from s17.person.behaviors.contact import IContactInfo
from s17.person.behaviors.user import IPloneUser


_PROJECT = 's17.person'
_PROFILE_ID = 's17.person:default'


def run_upgrades(context):
    ''' Run Upgrade steps
    '''
    if context.readDataFile('s17.person-default.txt') is None:
        return
    logger = logging.getLogger(_PROJECT)
    site = context.getSite()
    setup_tool = getToolByName(site, 'portal_setup')
    version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
    upgradeSteps = listUpgradeSteps(setup_tool, _PROFILE_ID, version)
    sorted(upgradeSteps, key=lambda step: step['sortkey'])

    for step in upgradeSteps:
        oStep = step.get('step')
        if oStep is not None:
            oStep.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (oStep.title,
                                                          _PROFILE_ID)
            setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
            logger.info(msg)


def demo_steps(context):
    """ Run steps to prepare a demo.
    """
    if context.readDataFile('s17.person-demo.txt') is None:
        return
    portal = context.getSite()
    portal.invokeFactory('Folder', 'Persons')
    folder = portal['Persons']
    list_users = [{'name': 'marcelo-santos', 'password': 'marcelo',
                   'number': '1', 'birthday': (1985, 2, 17)},
                  {'name': 'marcelo-alves', 'password': 'marcelo',
                   'number': '2', 'birthday': (1983, 6, 01)},
                  {'name': 'julia-alvarez', 'password': 'julia',
                   'number': '3', 'birthday': (1988, 10, 26)},
                  {'name': 'juan-perez', 'password': 'juan',
                   'number': '4', 'birthday': (1981, 1, 15)},
                  {'name': 'gustavo-roner', 'password': 'gustavo',
                   'number': '5', 'birthday': (1986, 2, 15)}]

    for user in list_users:
        create_user(user['name'], user['password'], portal)

    # Set behaviors to person
    behaviors = ['s17.person.behaviors.user.IPloneUser',
                 's17.person.behaviors.contact.IContactInfo']
    fti = queryUtility(IDexterityFTI, name='Person')
    fti.behaviors = tuple(behaviors)

    for user in list_users:
        person = user['name']
        fullname = person.split('-')
        birthday = user['birthday']
        image = os.path.join(
            os.path.dirname(__file__), 'profiles', 'demo', 'images', 'picture%s.png' % user['number'])
        data = getFile(image).read()
        folder.invokeFactory(
            'Person',
            person,
            birthday=datetime.date(datetime(birthday[0], birthday[1], birthday[2])),
            picture=NamedImage(data),
            given_name=fullname[0].capitalize(),
            surname=fullname[1].capitalize(),
            gender=u'm',
        )
        if (person == 'julia-alvarez'):
            folder[person].gender = 'f'
        p1_contact = IContactInfo(folder[person])
        p1_contact.emails = [
            {'category': u'work',
             'data': u'%s@simples.com.br' % person.replace('-', '.')},
            {'category': u'home',
             'data': u'%s@gmail.com' % person.replace('-', '.')},
        ]
        p1_contact.instant_messengers = [
            {'category': u'skype',
             'data': u'%s' % person.replace('-', '_')},
        ]
        p1_contact.telephones = [
            {'category': 'home', 'data': '+5511555.1213'},
            {'category': 'work', 'data': '+5511316.9876'},
        ]
        p1_ploneuser = IPloneUser(folder[person])
        p1_ploneuser.user_name = person
        folder[person].reindexObject()
        review_state = folder[person].portal_workflow.getInfoFor(folder[person], 'review_state')
        if not review_state == 'published':
            folder[person].portal_workflow.doActionFor(folder[person],
                                                       'publish')
    review_state = folder.portal_workflow.getInfoFor(folder, 'review_state')
    if not review_state == 'published':
        folder.portal_workflow.doActionFor(folder, 'publish')

    import transaction
    transaction.commit()


def create_user(username, password, portal):
    properties = {
        'username': username,
        'fullname': (u'%s' % username).encode("utf-8"),
        'email': u'%s@email.com' % username,
    }
    reg_tool = getToolByName(portal, 'portal_registration')
    reg_tool.addMember(username, password, properties=properties)
