from django import forms

from core.models import (
    InternetRating,
    Place,
    Rating
)


class PlaceTypeSearchForm(forms.ModelForm):

    class Meta:
        fields = ('place_type',)
        model = Place

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place_type'].required = False


class PlaceForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Place


class RatingForm(forms.ModelForm):

    class Meta:
        exclude = ('internet', 'place')
        model = Rating


class InternetRatingForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = InternetRating

    def clean(self):
        cleaned_data = super().clean()

        exists = cleaned_data['exists']
        speed = cleaned_data['speed']
        is_open = cleaned_data['is_open']
        password = cleaned_data['password']

        if not exists and (speed or is_open or password):
            self.add_error(
                'exists', 'This field is required when you fill the others '
                'below.')

        if exists and not speed:
            self.add_error(
                'speed', 'This field is required you check that there is '
                'internet.')

        if not is_open and not password:
            self.add_error(
                'password', 'This field is required you check that the '
                'internet is not open.')

        if is_open and password:
            self.add_error(
                'is_open', 'This field must be unchecked when you fill a '
                'password.')

        return cleaned_data
