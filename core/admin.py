from django.contrib import admin
from .models import Dish, Reservation, Order


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
	list_display = ("name", "price", "is_featured", "updated_at")
	list_filter = ("is_featured",)
	search_fields = ("name", "description")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
	list_display = ("name", "date", "time", "guests", "status")
	list_filter = ("status", "date")
	search_fields = ("name", "phone", "email")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("code", "phone", "status", "total", "placed_at")
	list_filter = ("status",)
	search_fields = ("code", "phone")
