# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0b2.dev0'
description = "A package containing a Dexterity content type and behaviors \
to represent a Person as a content in a Plone site."
long_description = (
    open("README.rst").read() + "\n" +
    open(os.path.join("docs", "INSTALL.rst")).read() + "\n" +
    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" +
    open(os.path.join("docs", "HISTORY.rst")).read()
)

setup(name='s17.person',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Office/Business",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='dexterity plone contenttypes',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['s17'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.z3cform.datagridfield',
          'five.grok',
          'Pillow',
          'plone.app.dexterity>=1.2.1',
          'plone.app.referenceablebehavior',
          'plone.behavior',
          'plone.dexterity',
          'plone.directives.dexterity',
          'plone.directives.form',
          'plone.namedfile[blobs]',
          'Products.CMFCore',
          'Products.CMFPlone>=4.2',
          'Products.GenericSetup',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.testing',
              'robotframework-selenium2library',
              'robotsuite',
          ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
