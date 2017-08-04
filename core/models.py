from django.db import models
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


class Rating(models.Model):

    place = models.ForeignKey('core.Place')

    internet = models.IntegerField(_('Internet'))
    food = models.IntegerField(_('Food'))
    customer_service = models.IntegerField(_('Customer Service'))
    price = models.IntegerField(_('Price'))
    comfort = models.IntegerField(_('Comfort'))
    noise = models.IntegerField(_('Noise'))
    overall = models.IntegerField(_('Overall Rating'))
