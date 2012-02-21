# -*- coding:utf-8 -*-
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.ZCatalog.exportimport import ZCatalogXMLAdapter
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects

from collective.person.catalog import IPersonCatalog


class PersonCatalogXMLAdapter(ZCatalogXMLAdapter):
    """
    Mode im- and exporter for PersonCatalog.
    """
    __used_for__ = IPersonCatalog
    # Explicita que esta classe adapta ICatalogPerson
    # para ISetupEnviron
    adapts(IPersonCatalog, ISetupEnviron)

    name = 'person_catalog'

    def _exportNode(self):
        """
        Export the settings as a DOM node.
        """
        node = ZCatalogXMLAdapter._exportNode(self)

        self._logger.info('Person Catalog settings exported.')
        return node

    def _importNode(self, node):
        """
        Import the settings from the DOM node.
        """
        ZCatalogXMLAdapter._importNode(self, node)

        self._logger.info('Person Catalog settings imported.')


def importPersonCatalog(context):
    """
    Import portal_personcatalog configuration.
    """

    site = context.getSite()
    tool = getToolByName(site, 'portal_personcatalog', None)

    if tool is None:
        logger = context.getLogger("collective.person")
        logger.info("Catalog not installed.")
        return

    importObjects(tool, '', context)


def exportPersonCatalog(context):
    """
    Export portal_personcatalog configuration.
    """

    site = context.getSite()
    tool = getToolByName(site, 'portal_personcatalog', None)
    if tool is None:
        logger = context.getLogger("collective.person")
        logger.info("Nothing to export.")
        return

    exportObjects(tool, '', context)
