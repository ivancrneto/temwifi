from django.test import TestCase
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy

from core import models


class PlaceModelTest(TestCase):

    def test_get_ratings(self):
        place = mommy.make('core.Place')
        mommy.make('core.Rating', place=place, overall=1)
        mommy.make('core.Rating', place=place, overall=2)
        mommy.make('core.Rating', overall=2)

        ratings = place.get_ratings()
        self.assertEqual(ratings['overall__avg'], 1.5)
        self.assertEqual(len(ratings), 5)

    def test_get_internet_summary_no_internet(self):
        place = mommy.make('core.Place')
        mommy.make('core.Rating', place=place, internet__exists=False)

        summary = place.get_internet_summary()
        self.assertEqual(summary, _('No'))

    def test_get_internet_summary_w_open_internet(self):
        place = mommy.make('core.Place')
        mommy.make(
            'core.Rating', place=place, internet__exists=True,
            internet__is_open=True,
            internet__speed=models.InternetRating.BETWEEN_3_AND_5_MBIT)

        summary = place.get_internet_summary()
        self.assertEqual(summary, _('Yes, Between 3 and 5 Mbps, Open'))

    def test_get_internet_summary_w_password_intenet(self):
        place = mommy.make('core.Place')
        mommy.make(
            'core.Rating', place=place, internet__exists=True,
            internet__is_open=False,
            internet__speed=models.InternetRating.BETWEEN_10_AND_20_MBIT,
            internet__password='abcde123')

        summary = place.get_internet_summary()
        self.assertEqual(
            summary, _('Yes, Between 10 and 20 Mbps, Password: abcde123'))


class RatingModelTest(TestCase):

    def test_ordering(self):
        rating1 = mommy.make('core.Rating')
        rating2 = mommy.make('core.Rating')

        ratings = models.Rating.objects.all()
        self.assertEqual(ratings[0], rating2)
        self.assertEqual(ratings[1], rating1)
