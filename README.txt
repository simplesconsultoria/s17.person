**************************************************************
collective.person
**************************************************************

.. contents:: Table of Contents
   :depth: 2

Overview
--------

A package containing a Dexterity content type and behaviors to represent a 
Person as a content in a Plone site.

Requirements
------------

    * Plone >=4.0.x (http://plone.org/products/plone)
    
    * Dexterity >=1.1 (http://plone.org/products/dexterity)

Installation
------------
    
To enable this product on a buildout based installation:

    1. Edit your buildout.cfg and add ``collective.person``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            collective.person


After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product (check its checkbox) and click the 'Install' button.

Uninstall -- This can be done from the same management screen, but only
if you installed it from the quick installer.

Note: You may have to empty your browser cache and save your resource
registries in order to see the effects of the product installation.

Example
-------

To give yourself an example you can use the demo profile within the
product. The steps to activate this profile you must do:

    1. Go to the zmi -> portal_setup.
    2. Click on ''Import'' tab.
    3. Select the profile ''collective.person: Demo profile'' from
       the drop down.
    4. Check the step ''collective.person: Demo steps'' and click the
       button ''import selected steps''.

Once you done the process you can see in you site a folder called ''Persons''
with five person items in wich each one have a base of information with a
picture.

With this option you can have a quick view to see what this product offers.

Sponsoring
----------

Development of this product was sponsored by :
    
    * `Simples Consultoria <http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * Simples Consultoria (products at simplesconsultoria dot com dot br) - 
      Implementation
    
