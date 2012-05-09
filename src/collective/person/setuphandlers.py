# -*- coding: utf-8 -*-
import logging

from Products.CMFCore.utils import getToolByName

from Products.GenericSetup.upgrade import listUpgradeSteps


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
    folder = portal['Empregados']
    list_users = [{'name':'marcelo-santos', 'password':'pass1'},
                  {'name':'rodrigo-alves', 'password':'pass2'},
                  {'name':'daniela-Alvarez', 'password':'pass3'},
                  {'name':'juan-perez', 'password':'pass4'},
                  {'name':'gustavo-rodriguez', 'password':'pass5'},]

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
        folder.invokeFactory('collective.person.person', person)
        folder[person].given_name = fullname[0].capitalize()
        folder[person].surname = fullname[1].capitalize()
        p1_contact = IContactInfo(folder[person])
        p1_contact.instant_messengers = [{'category': u'skype',
                                          'data': u'%s' % person.replace('-','_')}]
        p1_ploneuser = IPloneUser(folder[person])
        p1_ploneuser.user_name = person
        folder[person].reindexObject()

    import transaction
    transaction.commit()

    logger = logging.getLogger(PROJECTNAME)
    setup.run_upgrades_for_profile(PROFILE_ID, context, logger)


def create_user(username, password, portal):
    properties = {
    'username': username,
    'fullname': (u'%s' % username).encode("utf-8"),
    'email': u'%s@email.com' % username,
    }
    reg_tool = getToolByName(portal, 'portal_registration')
    reg_tool.addMember(username, password, properties=properties)