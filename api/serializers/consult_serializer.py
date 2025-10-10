from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class ConsultSerializer(serializers.ModelSerializer):
    visit_id = serializers.PrimaryKeyRelatedField(
        source="visit", queryset=models.Visit.objects.all(), write_only=True
    )
    visit = APISerializer.VisitSerializer(read_only=True)

    doctor_id = serializers.SlugRelatedField(
        source="doctor",
        slug_field="auth0_id",
        queryset=models.CustomUser.objects.all(),
        write_only=True,
    )
    doctor = APISerializer.UserSerializer(read_only=True)

    prescriptions = APISerializer.OrderSerializer(many=True, read_only=True)
    diagnosis = APISerializer.DiagnosisSerializer(many=True, read_only=True)

    class Meta:
        model = models.Consult
        fields = "__all__"
