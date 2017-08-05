from django.test import TestCase
from model_mommy import mommy

from core import views


class PlacesListViewTest(TestCase):

    def setUp(self):
        self.view = views.PlacesListView()

    def test_attr(self):
        self.assertIsInstance(self.view, views.ListView)
        self.assertEqual(self.view.model, views.Place)
        self.assertEqual(self.view.context_object_name, 'places')
        self.assertEqual(self.view.template_name, 'core/place_list.jinja')

    def test_get_queryset(self):
        place1 = mommy.make('core.Place')
        place2 = mommy.make('core.Place')
        mommy.make('core.Rating', place=place1)

        queryset = self.view.get_queryset()
        self.assertIn(place1, queryset)
        self.assertNotIn(place2, queryset)
