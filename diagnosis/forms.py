from django import forms
from clinicmodels.models import Diagnosis


class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['consult', 'details', 'category']
