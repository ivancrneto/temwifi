from collections import OrderedDict
from django.contrib import messages
from django.db.models import Avg, Q
from django.views.generic.list import ListView
from django.utils.translation import ugettext_lazy as _
from multi_form_view import MultiModelFormView

from core.forms import (
    PlaceForm,
    PlaceTypeSearchForm,
    InternetRatingForm,
    RatingForm
)
from core.models import Place


class PlacesListView(ListView):

    model = Place
    context_object_name = 'places'
    template_name = 'core/place_list.jinja'
    queryset = Place.objects.filter(ratings__isnull=False).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['place_type_search_form'] = PlaceTypeSearchForm()
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).annotate(
            Avg('ratings__price'))
        q = self.request.GET.get('q')
        place_type = self.request.GET.get('place_type')

        filtering = Q()

        if q:
            filtering |= (
                Q(address__icontains=q) |
                Q(city__icontains=q) |
                Q(state__icontains=q) |
                Q(country__icontains=q)
            )

            try:
                q = float(q)
            except ValueError:
                return queryset

            filtering |= Q(ratings__price__avg=q)
        if place_type:
            filtering &= Q(place_type=place_type)

        queryset = queryset.filter(filtering)

        return queryset


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

        messages.success(self.request, _('Rating saved with success.'))
        return super().forms_valid(forms)

    def get_forms(self):
        forms = super().get_forms()
        place_id = self.kwargs.get('place_id')
        if place_id:
            del forms['place_form']
        return forms

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['place_type_search_form'] = PlaceTypeSearchForm()

        form_keys = ['place_form', 'internet_rating_form', 'rating_form']
        ordered_forms = OrderedDict(
            [(k, context['forms'][k]) for k in form_keys
                if k in context['forms']])
        context['forms'] = ordered_forms

        place_id = self.kwargs.get('place_id')
        if place_id:
            context['place'] = Place.objects.filter(id=place_id).first()
        return context
