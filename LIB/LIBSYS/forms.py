from dataclasses import field
from django import forms
from .models import signupForm

class MemberForm(forms.ModelForm):
    class Meta:
        model = signupForm
        fields = "__all__"