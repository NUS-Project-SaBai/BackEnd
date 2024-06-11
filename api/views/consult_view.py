from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from api.serializers import *
from api.models import *
from rest_framework.response import Response


class ConsultView(APIView):
    def get(self, request, pk=None):
        pk = request.query_params.get("visit")
        if pk is not None:
            return self.get_object(pk)
        try:
            consults = Consult.objects.all()
            serializer = ConsultSerializer(consults, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def get_object(self, pk):
        try:
            consult = Consult.objects.filter(visit=pk)
            serializer = ConsultSerializer(consult, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({"message": str(e)}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        """
        POST request with multipart form to create a new consult
        :param request: POST request with the required parameters. Date parameters are accepted in the format 1995-03-30.
        :return: Http Response with corresponding status code
        """
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=500)

    def put(self, request, pk):
        """
        Update consult data based on the parameters
        :param request: POST with data
        :return: JSON Response with new data, or error
        """
        try:
            consult = Consult.objects.get(pk=pk)
            serializer = ConsultSerializer(consult, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception as e:
            return Response({"error": str(e)})

    def delete(self, request, pk):
        try:
            consult = Consult.objects.get(pk=pk)
            consult.delete()
            return Response({"message": "Deleted successfully"})
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)