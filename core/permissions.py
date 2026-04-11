from rest_framework.permissions import BasePermission

class IsWorkforce(BasePermission):
    message = "You don't belong to the the workforce which you are trying to access. Please contact the owner of said workforce."

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'members'):
            workspace = obj

        elif hasattr(obj, 'workspace'):
            workspace = obj.workspace

        elif hasattr(obj, 'project'):
            workspace = obj.project.workspace

        elif hasattr(obj, 'owner') and obj.owner == request.user:
            return True

        else:
            return False

        return workspace.members.filter(id=request.user.id).exists()