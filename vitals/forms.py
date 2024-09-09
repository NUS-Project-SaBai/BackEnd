from django import forms
from clinicmodels.models import Visit, Vitals


class VitalsForm(forms.ModelForm):
    visit = forms.ModelChoiceField(queryset=Visit.objects.all(), required=False)
    height = forms.DecimalField(required=False)
    weight = forms.DecimalField(required=False)
    systolic = forms.IntegerField(required=False)
    diastolic = forms.IntegerField(required=False)
    temperature = forms.DecimalField(required=False)
    hiv_positive = forms.BooleanField(required=False)
    ptb_positive = forms.BooleanField(required=False)
    hepc_positive = forms.BooleanField(required=False)
    diabetes_mellitus = forms.CharField(required=False)
    left_eye_pinhole = forms.CharField(required=False)
    right_eye_pinhole = forms.CharField(required=False)
    heart_rate = forms.IntegerField(required=False)
    urine_test = forms.CharField(required=False)
    hemocue_count = forms.DecimalField(required=False)
    blood_glucose = forms.DecimalField(required=False)
    left_eye_degree = forms.CharField(required=False)
    right_eye_degree = forms.CharField(required=False)
    eye_pressure = forms.CharField(required=False)
    cataracts = forms.CharField(required=False)
    others = forms.CharField(required=False)

    class Meta:
        model = Vitals
        fields = [
            "visit",
            "height",
            "weight",
            "systolic",
            "diastolic",
            "temperature",
            "hiv_positive",
            "ptb_positive",
            "hepc_positive",
            "heart_rate",
            "urine_test",
            "hemocue_count",
            "blood_glucose",
            "left_eye_degree",
            "right_eye_degree",
            "eye_pressure",
            "cataracts",
            "diabetes_mellitus",
            "left_eye_pinhole",
            "right_eye_pinhole",
            "others"
        ]
