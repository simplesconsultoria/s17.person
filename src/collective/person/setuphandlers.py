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

from collective.person.behaviors.contact import IContactInfo
from collective.person.behaviors.user import IPloneUser


_PROJECT = 'collective.person'
_PROFILE_ID = 'collective.person:default'


def run_upgrades(context):
    ''' Run Upgrade steps
    '''
    if context.readDataFile('collective.person-default.txt') is None:
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
    if context.readDataFile('collective.person-demo.txt') is None:
        return
    portal = context.getSite()
    portal.invokeFactory('Folder', 'Pessoas')
    folder = portal['Pessoas']
    list_users = [{'name':'marcelo-santos', 'password':'pass1', 'number': '1'},
                  {'name':'rodrigo-alves', 'password':'pass2', 'number': '2'},
                  {'name':'julia-Alvarez', 'password':'pass3', 'number': '3'},
                  {'name':'juan-perez', 'password':'pass4', 'number': '4'},
                  {'name':'gustavo-roner', 'password':'pass5', 'number': '5'}]

    for user in list_users:
        create_user(user['name'], user['password'], portal)

    # Set behaviors to person
    behaviors = ['collective.person.behaviors.user.IPloneUser',
                 'collective.person.behaviors.contact.IContactInfo']
    fti = queryUtility(IDexterityFTI,
                        name='collective.person.person')
    fti.behaviors = tuple(behaviors)

    for user in list_users:
        person = user['name']
        fullname = person.split('-')
        image = os.path.join(os.path.dirname(__file__), 'profiles', 'demo',
                             'images', 'picture%s.png' % user['number'])
        data = getFile(image).read()
        folder.invokeFactory('collective.person.person', person,
            birthday=datetime.date(datetime(1985, 2, 17)),
            picture=NamedImage(data),
            given_name=fullname[0].capitalize(),
            surname=fullname[1].capitalize(),
            gender=u'n/a',
            )
        p1_contact = IContactInfo(folder[person])
        p1_contact.emails = [{'category': u'work',
                                          'data': u'%s@simples.com.br' %
                                         person.replace('-', '.')},
                             {'category': u'home',
                                          'data': u'%s@gmail.com' %
                                         person.replace('-', '.')}]
        p1_contact.instant_messengers = [{'category': u'skype',
                                          'data': u'%s' %
                                         person.replace('-', '_')}]
        p1_contact.telephones = [{'category': 'home', 'data': '+5511555.1213'},
                                 {'category': 'work', 'data': '+5511316.9876'}]
        p1_ploneuser = IPloneUser(folder[person])
        p1_ploneuser.user_name = person
        folder[person].reindexObject()
        review_state = folder[person].portal_workflow.getInfoFor(
                                                            folder[person],
                                                            'review_state')
        if not review_state == 'published':
            folder[person].portal_workflow.doActionFor(folder[person],
                                                       'publish')

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
