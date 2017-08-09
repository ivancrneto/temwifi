from django.test import TestCase

from core import forms


class PlaceFormTest(TestCase):

    def setUp(self):
        self.form = forms.PlaceForm()

    def test_attr(self):
        meta = self.form._meta
        self.assertEqual(meta.model, forms.Place)


class RatingFormTest(TestCase):

    def setUp(self):
        self.form = forms.RatingForm()

    def test_attr(self):
        meta = self.form._meta
        self.assertEqual(meta.exclude, ('internet',))
        self.assertEqual(meta.model, forms.Rating)


class InternetFormTest(TestCase):

    def setUp(self):
        self.form = forms.InternetRatingForm()

    def test_attr(self):
        meta = self.form._meta
        self.assertEqual(meta.model, forms.InternetRating)
