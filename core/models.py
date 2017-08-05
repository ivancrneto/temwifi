from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _


class Place(models.Model):

    name = models.CharField(_('Name'), max_length=100)
    address = models.CharField(_('Address'), max_length=255)
    city = models.CharField(_('City'), max_length=30)
    state = models.CharField(_('State'), max_length=30)
    country = models.CharField(_('Country'), max_length=100)

    OTHER = 0
    COFFEE_SHOP = 10
    RESTAURANT = 20
    COWORKING = 30
    BOOKSTORE = 40

    TYPE_CHOICES = (
        (COFFEE_SHOP, _('Coffee Shop')),
        (RESTAURANT, _('Restaurant')),
        (COWORKING, _('Coworking')),
        (BOOKSTORE, _('Bookstore')),
        (OTHER, _('Other')),
    )
    place_type = models.IntegerField(choices=TYPE_CHOICES)

    class Meta:
        verbose_name_plural = _('Places')

    def get_ratings(self):
        return self.ratings.aggregate(Avg('overall'))


class InternetRating(models.Model):

    LESS_THAN_1_MBIT = 1
    BETWEEN_1_AND_3_MBIT = 3
    BETWEEN_3_AND_5_MBIT = 5
    BETWEEN_5_AND_10_MBIT = 10
    BETWEEN_10_AND_20_MBIT = 20
    BETWEEN_20_AND_50_MBIT = 50
    BETWEEN_50_AND_100_MBIT = 100
    MORE_THAN_100_MBIT = 1000

    SPEED_CHOICES = (
        (LESS_THAN_1_MBIT, _('Less than 1 Mbps')),
        (BETWEEN_1_AND_3_MBIT, _('Between 1 and 3 Mbps')),
        (BETWEEN_3_AND_5_MBIT, _('Between 3 and 5 Mbps')),
        (BETWEEN_5_AND_10_MBIT, _('Between 5 and 10 Mbps')),
        (BETWEEN_10_AND_20_MBIT, _('Between 10 and 20 Mbps')),
        (BETWEEN_20_AND_50_MBIT, _('Between 20 and 50 Mbps')),
        (BETWEEN_50_AND_100_MBIT, _('Between 50 and 100 Mbps')),
        (MORE_THAN_100_MBIT, _('More than 100 Mbps')),
    )

    exists = models.BooleanField(_('Exists'), default=False)
    speed = models.IntegerField(choices=SPEED_CHOICES, blank=True, null=True)
    is_open = models.BooleanField(_('Is Open'), default=False)
    password = models.CharField(_('Password'), max_length=200, null=True, blank=True)


class Rating(models.Model):

    place = models.ForeignKey('core.Place', related_name='ratings')
    internet = models.OneToOneField('core.InternetRating')

    food = models.TextField(_('Food'))
    drink = models.TextField(_('Drink'))
    customer_service = models.IntegerField(_('Customer Service'))
    price = models.IntegerField(_('Price'))
    comfort = models.IntegerField(_('Comfort'))
    noise = models.IntegerField(_('Noise'))
    overall = models.IntegerField(_('Overall Rating'))
