from collections import OrderedDict
from django.contrib import messages
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

    form_classes = {
        'rating_form': RatingForm,
        'internet_rating_form': InternetRatingForm,
        'place_form': PlaceForm,
    }
    template_name = 'core/add_rating.jinja'
    success_url = '/list/'

    def forms_valid(self, forms):
        internet_rating = forms['internet_rating_form'].save()
        if 'place_form' in forms:
            place = forms['place_form'].save()
        else:
            place = Place.objects.get(id=self.kwargs.get('place_id'))

        forms['rating_form'].instance.place = place
        forms['rating_form'].instance.internet = internet_rating
        forms['rating_form'].save()

        messages.success(self.request, 'Rating saved with success.')
        return super().forms_valid(forms)

    def get_forms(self):
        forms = super().get_forms()
        place_id = self.kwargs.get('place_id')
        if place_id:
            del forms['place_form']
        return forms

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        form_keys = ['place_form', 'internet_rating_form', 'rating_form']
        ordered_forms = OrderedDict(
            [(k, context['forms'][k]) for k in form_keys
                if k in context['forms']])
        context['forms'] = ordered_forms

        place_id = self.kwargs.get('place_id')
        if place_id:
            context['place'] = Place.objects.filter(id=place_id).first()
        return context
