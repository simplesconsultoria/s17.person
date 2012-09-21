# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

PROJECT = 's17.person'


def fromZero(context):
    ''' Upgrade from Zero to version 1000
    '''
    qi = getToolByName(context, 'portal_quickinstaller')
    qi.installProduct('collective.z3cform.datagridfield',
                      locked=0,
                      hidden=0,
                      profile='collective.z3cform.datagridfield:default')
