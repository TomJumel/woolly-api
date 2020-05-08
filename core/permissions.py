from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class CustomPermission(permissions.BasePermission):
    """
    CustomPermission class that can easily be customized
    """

    require_authentication = False
    allow_admin = True
    allow_read_only = False
    allow_create = False
    pass_for_obj = False

    # Final default values
    default = False
    default_obj = False

    # Customs permission check functions
    permission_functions = []
    object_permission_functions = []
    check_with_or = True

    @property
    def _check_functions(self):
        return any if self.check_with_or else all

    def has_permission(self, request, view) -> bool:
        # Action is not configured with as_view, ie not allowed
        if view.action is None:
            raise MethodNotAllowed(request.method)

        # Is Authenticated option
        if self.require_authentication and not request.user.is_authenticated:
            return False

        # Read Only option
        if self.allow_read_only and request.method in permissions.SAFE_METHODS:
            return True

        # Allow admin option
        if self.allow_admin and request.user.is_authenticated and request.user.is_admin:
            return True

        # Check all permission_functions
        if self.permission_functions:
            permission_gen = (func(request, view) for func in self.permission_functions)
            return self._check_functions(permission_gen)

        # Allow creation or not
        if view.action == 'create':
            return self.allow_create

        # Return True to get to object level permissions
        if self.pass_for_obj and view.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            return True

        return self.default

    def has_object_permission(self, request, view, obj) -> bool:
        # Allow admin option
        if self.allow_admin and request.user.is_authenticated and request.user.is_admin:
            return True

        # Read Only option
        if self.allow_read_only and request.method in permissions.SAFE_METHODS:
            return True

        # Check all object_permission_functions
        if self.object_permission_functions:
            permission_gen = (func(request, view, obj) for func in self.object_permission_functions)
            return self._check_functions(permission_gen)

        return self.default_obj


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only admins have the permission to modify, anyone can read
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin) \
            or (view.action and request.method in permissions.SAFE_METHODS)
