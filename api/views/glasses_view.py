from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models import Glasses, Visit
from api.serializers import GlassesSerializer, VisitSerializer


class GlassesView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        
        patient = request.query_params.get("patient", None)
        if patient is not None:
            visits = (
                Visit.objects.select_related("patient")
                .filter(patient_id=patient)
                .order_by("-id")
            )
            serializer = VisitSerializer(visits, many=True)
            return Response(serializer.data)

        glasses = Glasses.objects.all().order_by("-id")
        serializer = GlassesSerializer(glasses, many=True)
        return Response(serializer.data)
    
    def get_object(self, pk):
        glasses = get_object_or_404(Glasses, pk=pk)
        serializer = GlassesSerializer(glasses)
        return Response(serializer.data)

    def post(self, request):
        serializer = GlassesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        glasses = get_object_or_404(Glasses, pk=pk)

        data = {
            "left_glasses_degree": request.data.get("left_glasses_degree", glasses.left_glasses_degree),
            "right_glasses_degree": request.data.get("right_glasses_degree", glasses.right_glasses_degree),
            "visit_id": request.data.get("visit_id", glasses.visit_id),
        }

        serializer = GlassesSerializer(glasses, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)