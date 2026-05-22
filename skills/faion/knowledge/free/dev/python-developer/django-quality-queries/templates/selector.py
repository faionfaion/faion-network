# purpose: selector function skeleton centralising query optimisation
# consumes: Django models + relationship definitions
# produces: optimised QuerySet returned from one place, reused by views/admin/Celery
# depends-on: Django ORM (no extra deps)
# token-budget-impact: ~150 tokens

from django.db.models import Prefetch, QuerySet


def get_<entity>_list(*, user=None) -> QuerySet:
    """Return optimised queryset for the <entity> list endpoint.

    Owns select_related / prefetch_related so callers stay thin.
    """
    qs = <Model>.objects.all()
    if user is not None:
        qs = qs.filter(owner=user)
    return (
        qs
        .select_related("<fk_field>")  # one JOIN per single-valued relation accessed in loop
        .prefetch_related(
            Prefetch(
                "<related_set>",
                queryset=<RelatedModel>.objects.select_related("<inner_fk>"),
            ),
        )
        .order_by("-created_at")
    )
