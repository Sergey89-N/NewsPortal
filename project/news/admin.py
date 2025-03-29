from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Author, Category, Post, PostCategory, Comment


class AuthorAdmin(TranslationAdmin):
    list_display = ('user', 'rating',)


class CategoryAdmin(TranslationAdmin):
    list_display = ('name',)


class PostAdmin(TranslationAdmin):
    list_display = ('author', 'post_type', 'created_at', 'updated_at', 'title', 'content', 'rating',
              )

class PostCategoryAdmin(TranslationAdmin):
    list_display = ('post', 'category',)


class CommentAdmin(TranslationAdmin):
    list_display = ('post', 'user', 'text', 'created_at', 'rating',)

admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
