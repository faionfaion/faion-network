# purpose: HackSoft-style list selector skeleton — kwarg-only, QuerySet return
# consumes: Django Model + optional filter parameters
# produces: optimised QuerySet reused across views / tasks / admin
# depends-on: Django ORM, models module
# token-budget-impact: ~120 tokens

from django.db.models import Prefetch, QuerySet


def <entity>_list_for_<scope>(
    *,
    <scope>,
    status: str | None = None,
    limit: int | None = None,
) -> QuerySet[<Model>]:
    """Return the optimised QuerySet for <entity> in scope <scope>."""
    qs = (
        <Model>.objects
        .filter(<scope>=<scope>)
        .select_related("<fk_for_loop_access>")
        .prefetch_related(
            Prefetch(
                "<related_set>",
                queryset=<RelatedModel>.objects.select_related("<inner_fk>"),
            ),
        )
        .order_by("-created_at")
    )
    if status:
        qs = qs.filter(status=status)
    if limit:
        qs = qs[:limit]
    return qs
