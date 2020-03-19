from django import forms
from django_enumfield import enum
from .models import ATRCardType, StudentCard, RaspiTag, Student, Board


class RaspiTagForm(forms.Form):
    atr_hex = enum.EnumField(ATRCardType, default=ATRCardType.RASPI_TAG_ATR)
    uid = forms.CharField()


class RaspiTagFormModel(forms.ModelForm):
    # to change the form instead of model
    # title = forms.CharField(max_length=150)
    class Meta:
        model = RaspiTag
        fields = ["atr_hex", "uid"]

    def clean_title(self, *args, **kwargs):
        instance = self.instance
        title = self.cleaned_data.get('title')
        qs = RaspiTag.objects.filter(title__iexact=title)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)  # id=instance.id
        if qs.exists():
            raise forms.ValidationError("This title has already been used. Please try again.")
        return title
