# -*- coding: utf-8 -*-

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import s17.person
        self.loadZCML(package=s17.person)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 's17.person:default')


class FixtureDemo(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        portal.portal_workflow.setChainForPortalTypes(
             ['Folder', 's17.person.person'],
             ['simple_publication_workflow'])
        self.applyProfile(portal, 's17.person:demo')


FIXTURE = Fixture()
DEMO_FIXTURE = FixtureDemo()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='s17.person:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE, DEMO_FIXTURE, ),
    name='s17.person:Functional',
    )
