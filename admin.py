from django.contrib import admin

from .models import Booking, Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'featured']
    list_filter = ['category', 'featured']
    search_fields = ['title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'booking_date', 'booking_time', 'no_of_guests', 'user']
    list_filter = ['booking_date']
    search_fields = ['name']
