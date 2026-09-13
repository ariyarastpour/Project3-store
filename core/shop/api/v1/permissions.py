from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
<<<<<<< Updated upstream

        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user
=======
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user.user == request.user
>>>>>>> Stashed changes
