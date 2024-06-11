from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Vitals
from api.serializers import VitalsSerializer


class VitalsView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        
        try:
            visit = request.GET.get('visit', '')
            vitals = Vitals.objects.filter(visit=visit).all()
            serializer = VitalsSerializer(vitals)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)})
        
    def get_object(self, pk):
        try:
            vitals = Vitals.objects.get(pk=pk)
            serializer = VitalsSerializer(vitals)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)})

    def post(self, request):
        serializer = VitalsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            vitals = Vitals.objects.get(pk=pk)
            vitals.delete()
            return Response({"message": "Deleted successfully"})
        except Exception as e:
            return Response({"error": str(e)})
        