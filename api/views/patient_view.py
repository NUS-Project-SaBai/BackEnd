from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Patient
from api.serializers import PatientSerializer

class PatientView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            return self.get_object(pk)

        patient_name = request.query_params.get("name")
        
        patients = None

        try:
            if patient_name is None:
                patients = Patient.objects.all()
            else:
                patients = Patient.objects.filter(name=patient_name)
            
            if patients is None:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer = PatientSerializer(patients, many=True)

            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            serializer = PatientSerializer(patient)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)})

    def post(self, request):
        try:
            serializer = PatientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)})

    def delete(self, request, pk):
        try:
            patient = Patient.objects.get(pk=pk)
            patient.delete()
            return Response({"message": "Deleted successfully"})
        except Exception as e:
            return Response({"error": str(e)})


    


        
    
        
