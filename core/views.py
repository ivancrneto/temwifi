from collections import OrderedDict
from django.views.generic.list import ListView
from multi_form_view import MultiModelFormView

from core.forms import (
    PlaceForm,
    InternetRatingForm,
    RatingForm
)
from core.models import Place


class PlacesListView(ListView):

    model = Place
    context_object_name = 'places'
    template_name = 'core/place_list.jinja'
    queryset = Place.objects.filter(ratings__isnull=False).distinct()


class AddRatingView(MultiModelFormView):

    form_classes = OrderedDict([
        ('place_form', PlaceForm),
        ('rating_form', RatingForm),
        ('internet_rating_form', InternetRatingForm),
    ])
    template_name = 'core/add_rating.jinja'
    success_url = '/list/'

    def forms_valid(self, forms):
        internet_rating = forms['internet_rating_form'].save()
        forms['rating_form'].instance.internet = internet_rating
        forms['rating_form'].save()
        return super().forms_valid(forms)
