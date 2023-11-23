from django.contrib import admin

from api.models import Color


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'code']
    list_filter = ['id', 'title', 'slug', 'code']
    search_fields = ['title', 'code', 'slug']

