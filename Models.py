from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0)])
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title} (${self.price})'


class Booking(models.Model):
    """A single table reservation made by a user."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True
    )
    name = models.CharField(max_length=255)
    no_of_guests = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    booking_date = models.DateField()
    booking_time = models.TimeField()
    comment = models.CharField(max_length=1000, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['booking_date', 'booking_time']
        # Prevents the same slot from being double-booked under the same name.
        unique_together = ('name', 'booking_date', 'booking_time')

    def __str__(self):
        return f'{self.name} — {self.booking_date} {self.booking_time} ({self.no_of_guests} guests)'
