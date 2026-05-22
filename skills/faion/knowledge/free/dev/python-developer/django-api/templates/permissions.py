# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
Custom DRF permission classes: IsOrganizationMember, IsOwnerOrReadOnly, IsOwnerOrAdmin.
"""

from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsOrganizationMember(permissions.BasePermission):
    """
    Object-level: user must belong to the object's organization.
    Supports objects with .organization or .user FK.
    """

    message = "You don't have access to this resource."

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if hasattr(obj, "organization"):
            return obj.organization == request.user.organization
        if hasattr(obj, "user"):
            return obj.user.organization == request.user.organization
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level: write access only for owner; read access for authenticated users.
    Requires obj.user or obj.owner FK.
    """

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level: owner or staff/superuser can access.
    Unauthenticated users are always denied.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        if request.user.is_staff or request.user.is_superuser:
            return True
        owner = getattr(obj, "user", None) or getattr(obj, "owner", None)
        return owner == request.user
