There's a frood who really knows where his towel is
---------------------------------------------------

1.0b2 (2013-05-03)
^^^^^^^^^^^^^^^^^^

- Register static resource directory manually as Grok doesn't do it anymore.
  Package is now compatible with Plone 4.3. [hvelarde]

- Add image_thumb and tag methods to the content. This enables picture
  listing on folder_summary_view.  [ericof]


1.0b1 (2012-09-21)
^^^^^^^^^^^^^^^^^^

- Add plone.directives.dexterity as a dependency as required by Plone 4.3.
  [hvelarde]

- Deprecate use on Plone 4.1; we will support only Plone>=4.2. [hvelarde]

- Import getSite from zope.component to avoid dependency on
  zope.app.component. [hvelarde]

- Rename content type from "s17.person.person" to "Person". [hvelarde]

- Rename package from collective.person to s17.person. [hvelarde]


1.0a4 (2012-09-12)
^^^^^^^^^^^^^^^^^^

- Fix problem with collective.z3cform.datagridfield dependency
  install. [aleGpereira]


1.0a3 (2012-06-13)
^^^^^^^^^^^^^^^^^^

- Avoid crash when birthday year is prior to 1900. [jsbueno]

- Invalidate SCHEMA_CACHE in order to get the real behaviors. [ericof]


1.0a2 (2012-05-23)
^^^^^^^^^^^^^^^^^^^^^

- Package documentation was updated. [hvelarde]

- A demo profile was added. [aleGpereira]

- Fix a bug in email validator. [aleGpereira]

- Edit permission added to member linked with person object and test cases for
  this. [aleGpereira]

- A custom template assigned to person content type. [aleGpereira]

- Standardized image of person profile to 200px. [aleGpereira]


1.0a1 (2012-05-09)
^^^^^^^^^^^^^^^^^^

- Initial release.

