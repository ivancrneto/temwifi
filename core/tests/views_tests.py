from mox3 import mox
from django.test import RequestFactory, TestCase
from django.utils.translation import ugettext_lazy as _
from model_mommy import mommy

from core import views


class PlacesListViewTest(TestCase):

    def setUp(self):
        self.view = views.PlacesListView()
        self.view.request = RequestFactory().get('')

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


class AddRatingViewTest(TestCase):

    def setUp(self):
        self.view = views.AddRatingView()
        self.view.request = RequestFactory().post('')
        self.mock = mox.Mox()

    def test_attr(self):
        expected_form_classes = {
            'rating_form': views.RatingForm,
            'internet_rating_form': views.InternetRatingForm,
            'place_form': views.PlaceForm,
        }
        self.assertEqual(self.view.form_classes, expected_form_classes)
        self.assertEqual(self.view.template_name, 'core/add_rating.jinja')
        self.assertEqual(self.view.success_url, '/list/')

    def test_forms_valid(self):
        form1 = self.mock.CreateMockAnything()
        form2 = self.mock.CreateMockAnything()
        form3 = self.mock.CreateMockAnything()
        forms = {
            'internet_rating_form': form1,
            'rating_form': form2,
            'place_form': form3
        }

        self.mock.StubOutWithMock(form1, 'save')
        self.mock.StubOutWithMock(form2, 'save')
        self.mock.StubOutWithMock(form3, 'save')
        self.mock.StubOutWithMock(views, 'messages')
        self.mock.StubOutWithMock(views.MultiModelFormView, 'forms_valid')

        # Expected calls
        form1.save()
        form2.save()
        form3.save().AndReturn('mock place')
        views.messages.success(
            self.view.request, _('Rating saved with success.'))
        views.MultiModelFormView.forms_valid(forms)

        self.mock.ReplayAll()
        self.view.forms_valid(forms)
        self.mock.VerifyAll()
