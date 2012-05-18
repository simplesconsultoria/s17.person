# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.person
        self.loadZCML(package=collective.person)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.person:default')

class FixtureDemo(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        portal.portal_workflow.setChainForPortalTypes(
             ['Folder', 'collective.person.person'],
             ['simple_publication_workflow'])
        self.applyProfile(portal, 'collective.person:demo')


FIXTURE = Fixture()
DEMO_FIXTURE = FixtureDemo()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.person:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, DEMO_FIXTURE, ),
    name='collective.person:Functional',
    )
