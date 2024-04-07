from django.contrib import admin

from .models import Product, Comment, Category, Vote, Color

# Register your models here.
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Vote)

