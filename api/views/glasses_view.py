from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.serializers import GlassesSerializer
from api.models import Visit
from api.services import glasses_service


class GlassesView(APIView):
    def get(self, request):
        visit_id = request.query_params.get("visit")

        if visit_id:
            glasses = glasses_service.get_glasses_by_visit(visit_id)
        else:
            glasses = glasses_service.get_all_glasses()

        if not glasses:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GlassesSerializer(glasses, many=isinstance(glasses, list))
        return Response(serializer.data)

    def get_object(self, pk):
        glasses = glasses_service.get_glasses(pk)
        serializer = GlassesSerializer(glasses)
        return Response(serializer.data)

    def post(self, request):
        visit_id = request.data.get("visit_id")
        if not visit_id:
            return Response(
                {"detail": "visit_id is required in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        visit = get_object_or_404(Visit, id=visit_id)
        serializer = GlassesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        created = glasses_service.create_glasses(serializer.validated_data, visit)
        return Response(GlassesSerializer(created).data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        glasses = glasses_service.get_glasses(pk)
        filtered_data = {k: v for k, v in request.data.items() if v != ""}

        serializer = GlassesSerializer(glasses, data=filtered_data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated = glasses_service.update_glasses(glasses, serializer.validated_data)
        return Response(GlassesSerializer(updated).data)
