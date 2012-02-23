# -*- coding:utf-8 -*-
from zope import schema

from zope.annotation.interfaces import IAnnotations

from zope.component import adapts
from zope.interface import alsoProvides
from zope.interface import implements
from zope.interface import Interface
from zope.app.component.hooks import getSite
from zope.interface import Invalid, invariant

from plone.directives import form

from plone.app.content.interfaces import INameFromTitle

from Products.CMFCore.utils import getToolByName

from collective.person.content.person import IPerson

from collective.person import MessageFactory as _


def validate_user_name(value):
    site = getSite()
    pc = getToolByName(site, 'portal_personcatalog')
    results = pc.searchResults(object_provides=IPerson.__identifier__,
                               id=value)
    if len(results) > 0:
        return _(u'There is a person already asigned to this username')


class IPloneUser(form.Schema):
    '''Behavior for integration between a dexterity type and a
       Plone user
    '''

    user_name = schema.TextLine(
            title=_(u'Username'),
            description=_(u'Please inform a username to be used.'),
            #source="plone.principalsource.Principals",
            required=True,
        )

    @invariant
    def user_name_unique(data):
        """ Username must be unique on the site
        """
        context = getattr(data, '__context__', None)
        if context is not None:
            adapter = IPloneUser(context)
            if adapter.user_name == data.user_name:
                # No change, fine.
                return
        error = validate_user_name(data.user_name)
        if error:
            raise Invalid(error)


alsoProvides(IPloneUser, form.IFormFieldProvider)


class PloneUser(object):
    ''' adapter for IPloneUser '''

    implements(IPloneUser)
    adapts(IPerson)

    def __init__(self, context):
        self.context = context
        self.annotation = IAnnotations(self.context)

    @property
    def user_name(self):
        return self.annotation.get('collective.person.user_name', '')

    @user_name.setter
    def user_name(self, value):
        self.annotation['collective.person.user_name'] = value

    def getUser(self):
        ''' Return the Plone User related to this content
            or None if not available
        '''
        mt = getToolByName(self.context, 'portal_membership', None)
        if mt:
            member = mt.getMemberById(self.user_name)
            return member or None


class INameFromUserName(Interface):
    """Get the name from the user_name field value.

    This is really just a marker interface, automatically set by
    enabling the corresponding behavior.

    Note that when you want this behavior, then you MUST NOT enable
    the IDublinCore, IBasic, INameFromTitle or INameFromFile behaviors
    on your type.
    """


class NameFromUserName(object):
    implements(INameFromTitle)
    adapts(INameFromUserName)

    def __init__(self, context):
        self.context = context
        self.annotation = IAnnotations(self.context)

    @property
    def title(self):
        anno = self.annotation
        if anno and 'collective.person.user_name' in anno:
            return anno['collective.person.user_name']
