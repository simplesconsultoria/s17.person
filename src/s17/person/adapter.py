from zope.interface import Interface, implements

from zope.component import adapts

from borg.localrole.interfaces import ILocalRoleProvider

from Products.CMFCore.utils import getToolByName

from collective.person.behaviors.user import IPloneUser


class PersonLocalRoleAdapter(object):
    """ Calculate Editor roles based on person member owner.
    """
    implements(ILocalRoleProvider)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def getRoles(self, principal_id):
        localroles = []

        person = IPloneUser(self.context, None)
        if person:
            assigned_member = person.user_name
            if assigned_member == principal_id:
                localroles.append('Editor')

        return localroles

    def getAllRoles(self):
        """Returns all the local roles assigned in this context:
        (principal_id, [role1, role2])"""

        portal_membership = getToolByName(self.context, 'portal_membership')
        user = portal_membership.getAuthenticatedMember()

        properties = user.getUser()
        roles = properties.getRolesInContext(self.context)
        roles += self.getRoles(user.getId())
        return [(user.getId(), roles)]
