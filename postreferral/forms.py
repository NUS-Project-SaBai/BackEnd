from django import forms
from clinicmodels.models import PostReferral


class PostreferralForm(forms.ModelForm):
    class Meta:
        model = PostReferral
        fields = ['visit', 'recorder', 'remarks']
