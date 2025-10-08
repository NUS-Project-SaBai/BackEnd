from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.serializers import VillageSerializer
from api.services import village_service


class VillageView(APIView):
    def get(self, request, pk=None):
        if pk:
            village = village_service.get_village_by_id(pk)
            serializer = VillageSerializer(village)
            return Response(serializer.data)

        include_hidden = (
            request.query_params.get("include_hidden", "false").lower() == "true"
        )
        villages = village_service.get_all_villages(include_hidden=include_hidden)
        serializer = VillageSerializer(villages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VillageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = village_service.create_village(serializer.validated_data)
        return Response(VillageSerializer(created).data, status=status.HTTP_201_CREATED)

    # should include changing name(search replace), and also visibility of village (hidden or not)
    def patch(self, request, pk):
        village = village_service.get_village_by_id(pk)
        filtered_data = {k: v for k, v in request.data.items() if v != ""}
        serializer = VillageSerializer(village, data=filtered_data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated = village_service.edit_village(village, serializer.validated_data)
        return Response(VillageSerializer(updated).data)
