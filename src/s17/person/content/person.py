# -*- coding:utf-8 -*-
from Acquisition import aq_base
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

from Products.CMFCore.utils import getToolByName

from s17.person.utils import check_birthday
from s17.person.catalog import IPersonCatalog

from s17.person import MessageFactory as _


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
        date = obj.birthday
        # strftime method of datetime objects have an artificial
        # constraint on years prior to 1900 that is harmfull here.
        cooked = "%02d%02d" % (date.month, date.day)
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
def person_normalized_fullname(obj):
    ''' Normalize a person fullname
    '''
    norm = queryUtility(IIDNormalizer)
    if obj.fullname and norm:
        return norm.normalize(obj.fullname)

grok.global_adapter(person_normalized_fullname,
                    name="sortable_fullname")


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

    # Catalog Multiplex support
    def _catalogs(self):
        ''' catalogs we will use '''
        return [getToolByName(self, 'portal_catalog'),
                getToolByName(self, 'portal_personcatalog')]

    def indexObject(self):
        ''' index an object on all registered catalogs '''
        for c in self._catalogs():
            c.catalog_object(self)

    def unindexObject(self):
        ''' remove an object from all registered catalogs '''
        path = '/'.join(self.getPhysicalPath())
        for c in self._catalogs():
            c.uncatalog_object(path)

    def reindexObjectSecurity(self, skip_self=False):
        ''' reindex only security information on catalogs '''
        path = '/'.join(self.getPhysicalPath())
        for c in self._catalogs():
            for brain in c.unrestrictedSearchResults(path=path):
                brain_path = brain.getPath()
                if brain_path == path and skip_self:
                    continue
                # Get the object
                ob = brain._unrestrictedGetObject()

                # Recatalog with the same catalog uid.
                # _cmf_security_indexes in CMFCatalogAware
                c.reindexObject(ob,
                                idxs=self._cmf_security_indexes,
                                update_metadata=0,
                                uid=brain_path)

    def reindexObject(self, idxs=[]):
        ''' reindex object '''
        if idxs == []:
            # Update the modification date.
            if hasattr(aq_base(self), 'notifyModified'):
                self.notifyModified()
        for c in self._catalogs():
            if c is not None:
                c.reindexObject(self,
                                idxs=idxs)

    def Title(self):
        ''' Return a title from given_name and surname '''
        return self.fullname

    @property
    def title(self):
        ''' return fullname '''
        return self.fullname

    @title.setter
    def title(self, value):
        ''' we wont set a title here'''
        pass

    @property
    def fullname(self):
        ''' A person's fullname '''
        return '%s %s' % (self.given_name, self.surname)

    def image_thumb(self):
        ''' Return a thumbnail '''
        view = self.unrestrictedTraverse('@@images')
        return view.scale(fieldname='picture',
                          scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        ''' Return a tag to the image '''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='picture',
                        scale=scale,
                        css_class=css_class,
                        **kw)


class View(dexterity.DisplayForm):
    grok.context(IPerson)
    grok.require('zope2.View')
    grok.name('view')
