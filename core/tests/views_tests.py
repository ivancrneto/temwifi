from django.test import TestCase

from core import views


class PlacesListViewTest(TestCase):

    def setUp(self):
        self.view = views.PlacesListView()

    def test_attr(self):
        self.assertIsInstance(self.view, views.ListView)
        self.assertEqual(self.view.model, views.Place)
        self.assertEqual(self.view.context_object_name, 'places')
