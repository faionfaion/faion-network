# purpose: TBD-template-header
# consumes: input from methodology
# produces: output artefact
# depends-on: 01-core-rules.xml
# token-budget-impact: small

"""
StandardPagination (page-number) and TimelinePagination (cursor).
Reference these in REST_FRAMEWORK DEFAULT_PAGINATION_CLASS.
"""

from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Page-number pagination for general list endpoints.
    Supports ?page=N and ?page_size=N query params.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data) -> Response:
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def get_paginated_response_schema(self, schema: dict) -> dict:
        return {
            "type": "object",
            "properties": {
                "count": {"type": "integer"},
                "next": {"type": "string", "nullable": True},
                "previous": {"type": "string", "nullable": True},
                "results": schema,
            },
        }


class TimelinePagination(CursorPagination):
    """
    Cursor pagination for timeline/feed endpoints.
    Ordered by -created_at with -id tie-breaker.
    REQUIRES: ordering fields must be indexed in the DB.
    """

    page_size = 20
    ordering = ("-created_at", "-id")  # -id ensures stable ordering
    cursor_query_param = "cursor"
    page_size_query_param = "page_size"
    max_page_size = 50
