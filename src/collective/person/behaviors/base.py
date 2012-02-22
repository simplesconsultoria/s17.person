# -*- coding:utf-8 -*-
from zope.component import adapts
from zope.interface import implements

from plone.app.content.interfaces import INameFromTitle

from collective.person.content.person import IPerson


class INameFromFullName(INameFromTitle):
    """Get the name from the fullname field value.

    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    the IDublinCore, IBasic, INameFromTitle or INameFromFile behaviors
    on your type.
    """


class NameFromFullName(object):
    implements(INameFromFullName)
    adapts(IPerson)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.fullname
