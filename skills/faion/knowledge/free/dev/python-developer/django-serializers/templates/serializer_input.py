# purpose: DRF Input serializer skeleton (Create + Update) — explicit fields, no business logic
# consumes: a Model definition + the service contract
# produces: serializers passed `data=request.data` and validated by views
# depends-on: djangorestframework
# token-budget-impact: ~150 tokens

from rest_framework import serializers


class <Entity>CreateRequest(serializers.Serializer):
    """Input contract for creating a <Entity>."""

    name = serializers.CharField(required=True, allow_blank=False, max_length=120)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(required=False, default=True)
    # secret-like inputs MUST be write_only so accidental nesting cannot leak them
    password = serializers.CharField(required=True, min_length=12, write_only=True)

    def validate_name(self, value: str) -> str:
        # SHAPE-ONLY validation. No DB, no service calls.
        if value.strip() != value:
            raise serializers.ValidationError("must not contain leading/trailing whitespace")
        return value


class <Entity>UpdateRequest(serializers.Serializer):
    """Input contract for partial updates (PATCH)."""

    name = serializers.CharField(required=False, allow_blank=False, max_length=120)
    email = serializers.EmailField(required=False)
    is_active = serializers.BooleanField(required=False)
