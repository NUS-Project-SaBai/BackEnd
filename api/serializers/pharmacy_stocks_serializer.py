from rest_framework import serializers

class PharmacyStockSerializer(serializers.Serializer):
    medicine_id = serializers.IntegerField(source='id')
    medicine_name = serializers.CharField()
    quantity = serializers.IntegerField()
    code = serializers.CharField()