from django import forms
from clinicmodels.models import Consult


class ConsultForm(forms.ModelForm):
    class Meta:
        model = Consult
        fields = ['visit', 'doctor', 'past_medical_history', 'consultation', 'plan',
                  'referred_for', 'referral_notes', 'remarks']
