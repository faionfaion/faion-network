# users/selectors/user_selectors.py — Selector layer template (HackSoft pattern)
# Rules: read-only, return QuerySet or typed value, no mutations, eager loading included.

from datetime import timedelta
from typing import Optional

from django.db.models import Q, QuerySet
from django.utils import timezone

from users.models import User


def get_all() -> QuerySet[User]:
    """All users (unsorted)."""
    return User.objects.all()


def get_active() -> QuerySet[User]:
    """All active users."""
    return User.objects.filter(is_active=True)


def get_by_id(user_id: int) -> Optional[User]:
    """Single user by primary key or None."""
    return User.objects.filter(id=user_id).first()


def get_by_email(email: str) -> Optional[User]:
    """Single user by email (case-insensitive) or None."""
    return User.objects.filter(email__iexact=email).first()


def email_exists(email: str) -> bool:
    """True if email is already registered."""
    return User.objects.filter(email__iexact=email).exists()


def search(query: str) -> QuerySet[User]:
    """Search active users by name or email."""
    return User.objects.filter(
        Q(first_name__icontains=query)
        | Q(last_name__icontains=query)
        | Q(email__icontains=query),
        is_active=True,
    )


def get_recent(days: int = 30) -> QuerySet[User]:
    """Users registered in last N days."""
    since = timezone.now() - timedelta(days=days)
    return User.objects.filter(date_joined__gte=since)


def get_with_orders() -> QuerySet[User]:
    """Active users with orders prefetched (avoids N+1)."""
    return User.objects.filter(is_active=True).prefetch_related("orders")
