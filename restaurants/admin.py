from django.contrib import admin
from .models import Cuisine, Restaurant, Course


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo', 'opening_hours', 'min_order_amount']
    search_fields = ['name', 'cuisines', 'description']
    list_filter = ['name', 'cuisines']
    ordering = ['name']
    empty_value_display = '-empty-'


class CuisineAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    ordering = ['name']
    search_fields = ['name']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'restaurant', 'price',
                    'is_spicy', 'is_glutenfree', 'is_vegan']
    list_filter = ['is_spicy', 'is_glutenfree', 'is_vegan']
    ordering = ['name']
    search_fields = ['name', 'description']


admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Course, CourseAdmin)
