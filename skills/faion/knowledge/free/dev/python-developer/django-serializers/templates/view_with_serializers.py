# purpose: view skeleton chaining Input serializer -> service -> Output serializer
# consumes: Input + Output serializers, service function, selector for list endpoint
# produces: APIView with consistent 201/200/400 responses
# depends-on: djangorestframework + apps.<x>.services + apps.<x>.selectors
# token-budget-impact: ~160 tokens

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.<x> import selectors, services
from apps.<x>.serializers import (
    <Entity>CreateRequest,
    <Entity>ListResponse,
    <Entity>Response,
    <Entity>UpdateRequest,
)


class <Entity>CreateApi(APIView):
    def post(self, request):
        serializer = <Entity>CreateRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        entity = services.<entity>_create(**serializer.validated_data)
        return Response(<Entity>Response(entity).data, status=status.HTTP_201_CREATED)


class <Entity>ListApi(APIView):
    def get(self, request):
        qs = selectors.<entity>_list_for_user(user=request.user)
        # pagination omitted for brevity; wire DRF paginator here
        payload = {"count": qs.count(), "next": None, "previous": None, "results": list(qs)}
        return Response(<Entity>ListResponse(payload).data, status=status.HTTP_200_OK)
