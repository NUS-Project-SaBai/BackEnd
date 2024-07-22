from rest_framework import serializers
from api import models
from api import serializers as APISerializer


class ConsultSerializer(serializers.ModelSerializer):
    # visit = serializers.PrimaryKeyRelatedField(
    #     queryset=models.Visit.objects.all())
    doctor = serializers.SlugRelatedField(
        slug_field='auth0_id',
        queryset=models.CustomUser.objects.all()
    )
    prescriptions = APISerializer.OrderSerializer(many=True, read_only=True)
    diagnosis = APISerializer.DiagnosisSerializer(many=True, read_only=True)

    class Meta:
        model = models.Consult
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["visit"] = APISerializer.VisitSerializer(
            instance.visit).data
        representation["doctor"] = APISerializer.UserSerializer(
            instance.doctor).data
        return representation

    # def create(self, validated_data):
    #     print(validated_data)
    #     consult_data = validated_data.pop('consult')
    #     orders_data = validated_data.pop('orders', [])
    #     diagnosis_data = validated_data.pop('diagnoses', [])
    #     # print(consult_data)
    #     print(orders_data)
    #     print(diagnosis_data)

    #     # Create the Consult instance
    #     consult = models.Consult.objects.create(**validated_data)

    #     # Create related orders
    #     for order_data in orders_data:
    #         models.Order.objects.create(consult=consult, **order_data)

    #     # Create related diagnosis
    #     for diagnosis_data in diagnosis_data:
    #         models.Diagnosis.objects.create(consult=consult, **diagnosis_data)

    #     return consult
