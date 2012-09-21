# -*- coding: utf-8 -*-
from Globals import InitializeClass

from zope.interface import Interface
from zope.interface import implements

from Products.CMFPlone.CatalogTool import CatalogTool


class IPersonCatalog(Interface):
    """A specialized catalog to deal with Persons
    """


class PersonCatalog(CatalogTool):
    """A specialized catalog to deal with Persons
    """

    id = 'portal_personcatalog'
    portal_type = meta_type = 'PersonCatalog'
    implements(IPersonCatalog)

    def getId(self):
        return self.id


InitializeClass(PersonCatalog)
