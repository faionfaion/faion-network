# purpose: HackSoft-style single-object selector — kwarg-only, raises DoesNotExist
# consumes: Django Model + identifier + optional ownership scope
# produces: a single Model instance (or DoesNotExist propagates to caller / 404)
# depends-on: Django ORM
# token-budget-impact: ~110 tokens


def <entity>_get(
    *,
    <entity>_id: int,
    user=None,
) -> <Model>:
    """Return the single <entity> by id, optionally scoped to a user.

    Raises <Model>.DoesNotExist when not found / not owned by the user.
    NEVER returns None — callers convert to 404 (DRF) or get_object_or_404 (vanilla).
    """
    qs = (
        <Model>.objects
        .select_related("<fk_1>", "<fk_2>")
        .prefetch_related("<reverse_or_m2m>__<nested>")
    )
    if user is not None:
        qs = qs.filter(<owner_field>=user)
    return qs.get(pk=<entity>_id)
