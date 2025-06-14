from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Vitals
from api.serializers import VitalsSerializer


class VitalsView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        vitals = Vitals.objects.all()
        visit = request.query_params.get("visit", "")
        if visit:
            vitals = Vitals.objects.filter(visit=visit)
        serializer = VitalsSerializer(vitals, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        vitals = Vitals.objects.get(pk=pk)
        serializer = VitalsSerializer(vitals)
        return Response(serializer.data)

    def post(self, request):
        serializer = VitalsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk=None):
        if pk is not None:
            vital = Vitals.objects.get(pk=pk)
            return self.patch_object(request, vital)

        vital = Vitals.objects.all()
        visit = request.query_params.get("visit", "")
        if visit:
            vital = vital.filter(visit=visit).first()
        return self.patch_object(request, vital)

    def patch_object(self, request, vital):
        filtered_request_data = dict(
            filter(lambda item: item[1] != "", request.data.items())
        )
        serializer = VitalsSerializer(vital, data=filtered_request_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        vitals = Vitals.objects.get(pk=pk)
        vitals.delete()
        return Response({"message": "Deleted successfully"})
