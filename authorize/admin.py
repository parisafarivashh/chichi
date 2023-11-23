from django.contrib import admin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'first_name',
        'last_name',
        'avatar',
        'phone',
        'email',
        'date_joined',
        'is_admin',
    ]
    list_filter = ['id', 'title', 'first_name', 'last_name', 'is_admin', 'email']
    search_fields = ['id', 'title', 'first_name', 'last_name', 'email']
    readonly_fields = ['password']

