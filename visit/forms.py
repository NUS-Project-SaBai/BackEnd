from django import forms
from clinicmodels.models import Visit


class VisitForm(forms.ModelForm):

    class Meta:
        model = Visit
        fields = ['patient', 'status']
