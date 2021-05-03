from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['docfile']
        widgets = {'docfile': forms.FileInput(
            attrs={'style': 'display: none;', 'class': 'form-control', 'required': False, }
        )}
