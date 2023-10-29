from django.contrib import admin

from src.models import User, Color


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'first_name', 'last_name', 'avatar',
                    'phone', 'email', 'date_joined', 'is_admin']
    list_filter = ['id', 'title', 'first_name', 'last_name', 'is_admin',
                   'email']
    search_fields = ['id', 'title', 'first_name', 'last_name', 'email']
    readonly_fields = ['password']


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'code']
    list_filter = ['id', 'title', 'slug', 'code']
    search_fields = ['title', 'code', 'slug']

