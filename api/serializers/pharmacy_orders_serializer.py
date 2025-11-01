from rest_framework import serializers


class PatientMiniSerializer(serializers.Serializer):
    patient_id = serializers.CharField()
    name = serializers.CharField()
    picture_url = serializers.CharField(allow_null=True, allow_blank=True)
    village_prefix = serializers.CharField()


class OrderMiniSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    medication_name = serializers.CharField()
    medication_code = serializers.CharField()
    quantity_changed = serializers.IntegerField()
    is_low_stock = serializers.BooleanField()
    notes = serializers.CharField()


class DiagnosisMiniSerializer(serializers.Serializer):
    category = serializers.CharField()
    details = serializers.CharField()


class VisitBundleSerializer(serializers.Serializer):
    orders = serializers.ListSerializer(child=OrderMiniSerializer())
    diagnoses = serializers.ListSerializer(child=DiagnosisMiniSerializer())
    visit_id = serializers.IntegerField()
    visit_date = serializers.DateTimeField()


class PharmacyOrdersPatientSerializer(serializers.Serializer):
    patient = PatientMiniSerializer()
    data = serializers.ListSerializer(child=VisitBundleSerializer())
