from django.views.generic.list import ListView

from core.models import Place


class PlacesListView(ListView):

    model = Place
    context_object_name = 'places'
    template_name = 'core/place_list.jinja'
    queryset = Place.objects.filter(ratings__isnull=False).distinct()
