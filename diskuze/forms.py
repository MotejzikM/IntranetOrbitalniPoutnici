from .models import Zprava, Diskuze
from django import forms
from django.utils.translation import gettext_lazy as _

class ZpravaForm(forms.ModelForm):
    class Meta:
        model = Zprava
        fields = ['nazev', 'obsah']
        widgets = {
            'obsah': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nazev': _("Název zprávy"),
            'obsah': _("Obsah zprávy"),
        }
        exclude = ['datum_vytvoreni']

        error_messages = {
            'obsah': {
                'required': _("Obsah zprávy je povinný."),
            },
        }

class DiskuzeForm(forms.ModelForm):
    class Meta:
        model = Diskuze
        fields = ['nazev', 'popis']
        widgets = {
            'popis': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nazev': _("Název diskuze"),
            'popis': _("Popis diskuze"),
        }
        error_messages = {
            'nazev': {
                'required': _("Název diskuze je povinný."),
            },
        }