from django import forms
from clinicmodels.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "village_prefix",
            "name",
            "identification_number",
            "contact_no",
            "gender",
            "date_of_birth",
            "drug_allergy",
            "face_encodings",
            "picture",
        ]
