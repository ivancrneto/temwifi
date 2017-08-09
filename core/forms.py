from django import forms

from core.models import (
    InternetRating,
    Place,
    Rating
)


class PlaceForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Place


class RatingForm(forms.ModelForm):

    class Meta:
        exclude = ('internet',)
        model = Rating


class InternetRatingForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = InternetRating
