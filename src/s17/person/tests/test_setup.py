# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.site.hooks import setSite

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from s17.person.testing import INTEGRATION_TESTING

PROJECTNAME = 's17.person'


class BaseTestCase(unittest.TestCase):
    """base test case to be used by other tests"""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.pp = getattr(self.portal, 'portal_properties')
        self.wt = getattr(self.portal, 'portal_workflow')
        self.st = getattr(self.portal, 'portal_setup')
        self.setUpUser()


class TestInstall(BaseTestCase):
    """ensure product is properly installed"""

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_installed_datagridfield(self):
        dependency = 'collective.z3cform.datagridfield'
        self.assertTrue(self.qi.isProductInstalled(dependency),
                        '%s not installed' % dependency)

    def test_catalog_installed(self):
        self.assertTrue('portal_personcatalog' in self.portal.objectIds(),
                        'Catalog not installed')

    def test_css_registry(self):
        portal_css = self.portal.portal_css
        resources = portal_css.getResourceIds()
        self.assertTrue('++resource++s17.person.stylesheets/s17.person.css' in resources)


class TestUninstall(BaseTestCase):
    """ensure product is properly uninstalled"""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_css_registry(self):
        portal_css = self.portal.portal_css
        resources = portal_css.getResourceIds()
        self.assertFalse('++resource++s17.person.stylesheets/s17.person.css' in resources)
