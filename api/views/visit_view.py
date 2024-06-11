from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Visit
from api.serializers import VisitSerializer


class VisitView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        
        try:
            visits = Visit.objects.select_related("patient").all()
            patient = request.query_params.get('patient', '')
            if patient:
                visits = visits.filter(patient=patient)
            serializer = VisitSerializer(visits, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)})

    def get_object(self, pk):
        try:
            visit = Visit.objects.get(pk=pk)
            serializer = VisitSerializer(visit)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)})
        
    def post(self, request):
        serializer = VisitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
            visit.delete()
            return Response({"message": "Deleted successfully"})
        except Exception as e:
            return Response({"error": str(e)})
