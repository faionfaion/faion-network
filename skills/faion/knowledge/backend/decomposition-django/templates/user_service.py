# users/services/user_service.py — Service layer template (HackSoft pattern)
# Rules: keyword-only args, dataclass inputs, @transaction.atomic only on multi-write ops,
#        no HTTP concepts, no serializer imports.

from dataclasses import dataclass
from typing import Optional

from django.db import transaction

from users.models import User


@dataclass
class UserCreateInput:
    """Input for user creation. Validated before reaching service."""
    email: str
    password: str
    first_name: str = ""
    last_name: str = ""


@dataclass
class UserUpdateInput:
    """Input for user update. All fields optional."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


@transaction.atomic
def user_create(*, data: UserCreateInput) -> User:
    """
    Create new user.

    Raises:
        ValueError: If email already registered.
    """
    if User.objects.filter(email__iexact=data.email).exists():
        raise ValueError("Email already registered")

    return User.objects.create_user(
        email=data.email,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
    )


def user_update(*, user: User, data: UserUpdateInput) -> User:
    """Update user fields. Only saves fields that changed."""
    fields_to_update = []

    if data.first_name is not None:
        user.first_name = data.first_name
        fields_to_update.append("first_name")

    if data.last_name is not None:
        user.last_name = data.last_name
        fields_to_update.append("last_name")

    if data.phone is not None:
        user.phone = data.phone
        fields_to_update.append("phone")

    if fields_to_update:
        user.save(update_fields=fields_to_update + ["updated_at"])

    return user


def user_deactivate(*, user: User) -> None:
    """Soft-delete user by marking inactive."""
    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])
