from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('text',)
    list_display = ('id', 'title', 'text', 'is_published',)
    list_display_links = ('id', 'title',)
    list_editable = ('text', 'is_published',)
    list_filter = ('created_at',)
    empty_value_display = 'Не задано'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    empty_value_display = 'Не задано'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = 'Не задано'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'author', 'is_published']
    empty_value_display = '-пусто-'
