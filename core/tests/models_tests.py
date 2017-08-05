from django.test import TestCase
from model_mommy import mommy


class PlaceModelTest(TestCase):

    def test_get_ratings(self):
        place = mommy.make('core.Place')
        mommy.make('core.Rating', place=place, overall=1)
        mommy.make('core.Rating', place=place, overall=2)
        mommy.make('core.Rating', overall=2)

        ratings = place.get_ratings()
        self.assertEqual(ratings['overall__avg'], 1.5)
        self.assertEqual(len(ratings), 1)
