# purpose: DRF Output serializer skeleton — explicit allowlist, never `__all__`
# consumes: Model instance(s) from a selector
# produces: response body wrapping a model with safe field set
# depends-on: djangorestframework
# token-budget-impact: ~140 tokens

from rest_framework import serializers


class <Entity>Response(serializers.Serializer):
    """Output contract for a single <Entity>. Lists exposed fields explicitly."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    # DO NOT add password / token / secret / is_staff / mfa_secret


class <Entity>ListItem(serializers.Serializer):
    """Compact representation for list endpoints — fewer fields than detail."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class <Entity>ListResponse(serializers.Serializer):
    """List wrapper with pagination metadata."""

    count = serializers.IntegerField(read_only=True)
    next = serializers.URLField(read_only=True, allow_null=True)
    previous = serializers.URLField(read_only=True, allow_null=True)
    results = <Entity>ListItem(many=True, read_only=True)
