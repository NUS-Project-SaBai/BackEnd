from rest_framework import serializers
from api import models
from sabaibiometrics.settings import OFFLINE, CLOUDINARY_URL, BACKEND_API


class PatientSerializer(serializers.ModelSerializer):
    patient_id = serializers.SerializerMethodField()
    filter_string = serializers.SerializerMethodField()
    confidence = serializers.SerializerMethodField()
    picture_url = serializers.SerializerMethodField()

    # Explicitly declare these to allow DRF to pass them through to the model
    picture = serializers.ImageField(required=False, allow_null=True)
    offline_picture = serializers.ImageField(required=False, allow_null=True)
    
    last_visit_date = serializers.DateTimeField(read_only=True)
    last_visit_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Patient
        fields = [
            "pk",
            "village_prefix",
            "name",
            "identification_number",
            "contact_no",
            "gender",
            "date_of_birth",
            "poor",
            "bs2",
            "sabai",
            "drug_allergy",
            "face_encodings",
            "picture",
            "offline_picture",
            "picture_url",  # 👈 new field for display use
            "patient_id",
            "filter_string",
            "confidence",
            "last_visit_date",
            "last_visit_id"
        ]

    def get_patient_id(self, obj):
        return f"{obj.village_prefix}{obj.pk:04d}"

    def get_filter_string(self, obj):
        return f"{obj.village_prefix}{obj.pk:04d} {obj.village_prefix}{obj.pk} {obj.contact_no} {obj.name}"

    def get_confidence(self, obj):
        confidence_dict = self.context.get("confidence", {})
        return confidence_dict.get(obj.face_encodings, "")

    def get_picture_url(self, obj):
        if OFFLINE and obj.offline_picture:
            return f"{BACKEND_API}{obj.offline_picture.url}"
        elif obj.picture:
            return f"{CLOUDINARY_URL}/{obj.picture}"
        return None
    
    # def get_last_visit_date(self, obj):
    #     return obj.last_visit_date

    # def get_last_visit_id(self, obj):
    #     return obj.last_visit_id
