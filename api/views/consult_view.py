from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Consult
from api.serializers import ConsultSerializer
from sabaibiometrics.utils import jwt_decode_token


class ConsultView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)
        consults = Consult.objects.all()
        visit_key = request.query_params.get("visit", "")
        if visit_key:
            consults = consults.filter(visit=visit_key)
        serializer = ConsultSerializer(consults, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        consult = Consult.objects.filter(pk=pk).first()
        serializer = ConsultSerializer(consult)
        return Response(serializer.data)

    def post(self, request):
        if request.headers["Authorization"]:
            token = request.headers["Authorization"].split(" ")[1]
            payload = jwt_decode_token(token)
            request.data["doctor"] = payload["sub"]
        serializer = ConsultSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def patch(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        serializer = ConsultSerializer(
            consult, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        consult = Consult.objects.get(pk=pk)
        consult.delete()
        return Response({"message": "Deleted successfully"})
