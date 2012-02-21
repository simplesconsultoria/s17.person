# -*- coding:utf-8 -*-
from five import grok
from zope import schema
from zope.component import queryUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from plone.directives import dexterity

from plone.directives import form
from plone.indexer import indexer

from plone.i18n.normalizer.interfaces import IIDNormalizer

from plone.namedfile.field import NamedImage

from collective.person.utils import check_birthday
from collective.person.catalog import IPersonCatalog

from collective.person import MessageFactory as _


gender_options = SimpleVocabulary(
    [SimpleTerm(value=u'f', title=_(u'Female')),
     SimpleTerm(value=u'm', title=_(u'Male')),
     SimpleTerm(value=u'n/a', title=_(u'Rather not say'))])


class IPerson(form.Schema):
    """ A representation of a Person
    """

    given_name = schema.TextLine(
        title=_(u"First Name"),
        description=_(u"First name of this person."),
        required=True,
        )

    surname = schema.TextLine(
        title=_(u"Surname"),
        description=_(u"Surname of this person."),
        required=True,
        )

    gender = schema.Choice(
        title=_(u"Gender"),
        description=_(u""),
        required=False,
        source=gender_options,
        )

    birthday = schema.Date(
        title=_(u"Birthday"),
        description=_(u"Birthday of this person."),
        required=False,
        constraint=check_birthday,
        )

    picture = NamedImage(
        title=_(u"Portrait"),
        description=_(u"Please provide a portrait for this person."),
        required=False,
        )


@indexer(IPerson, IPersonCatalog)
def person_cooked_birthday(obj):
    ''' Prepare a person's birthday date to be
        indexed in the format mmdd so we can order it
        in a easy way
    '''
    if obj.birthday:
        cooked = obj.birthday.strftime('%m%d')
        return cooked

grok.global_adapter(person_cooked_birthday,
                    name="cooked_birthday")


@indexer(IPerson, IPersonCatalog)
def person_normalized_given_name(obj):
    ''' Normalize a person given_name
    '''
    norm = queryUtility(IIDNormalizer)
    if obj.given_name and norm:
        return norm.normalize(obj.given_name)

grok.global_adapter(person_normalized_given_name,
                    name="sortable_given_name")


@indexer(IPerson, IPersonCatalog)
def person_normalized_surname(obj):
    ''' Normalize a person surname
    '''
    norm = queryUtility(IIDNormalizer)
    if obj.surname and norm:
        return norm.normalize(obj.surname)

grok.global_adapter(person_normalized_surname,
                    name="sortable_surname")


@indexer(IPerson, IPersonCatalog)
def person_has_portrait(obj):
    ''' Return Tr if the person has a portrait
    '''
    if obj.portrait:
        return True

grok.global_adapter(person_has_portrait,
                    name="has_portrait")


class Person(dexterity.Item):
    """ A Person
    """
    grok.implements(IPerson)

    def Title(self):
        ''' Return a title from given_name and surname '''
        return '%s %s' % (self.given_name, self.surname)

    @property
    def title(self):
        return self.Title()

    @title.setter
    def title(self, value):
        # We make sure our title is defined **only** by
        # Title function
        pass

    @property
    def fullname(self):
        ''' A person's fullname '''
        return self.Title()
