from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models import Glasses, Visit
from api.serializers import GlassesSerializer, VisitSerializer


class GlassesView(APIView):
    def get(self, request):
        visit_id = request.query_params.get("visit")
        if visit_id:
            glasses = Glasses.objects.filter(visit_id=visit_id)
        else:
            glasses = Glasses.objects.all()
        serializer = GlassesSerializer(glasses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_object(self, pk):
        glasses = get_object_or_404(Glasses, pk=pk)
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
        serializer.save(visit=visit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        glasses = get_object_or_404(Glasses, pk=pk)
        serializer = GlassesSerializer(glasses, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)