from django import forms

from core.models import InternetRating, Rating


class RatingForm(forms.ModelForm):

    class Meta:
        exclude = ('internet',)
        model = Rating


class InternetForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = InternetRating
