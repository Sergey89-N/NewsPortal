from modeltranslation.translator import translator, TranslationOptions
from .models import Author, Category, Post, PostCategory, Comment


class AuthorTranslationOptions(TranslationOptions):
    fields = ('user', 'rating',)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class PostTranslationOptions(TranslationOptions):
    fields = ('author', 'post_type', 'created_at', 'updated_at', 'title', 'content', 'rating',
              )

class PostCategoryTranslationOptions(TranslationOptions):
    fields = ('post', 'category',)


class CommentTranslationOptions(TranslationOptions):
    fields = ('post', 'user', 'text', 'created_at', 'rating',)


translator.register(Author, AuthorTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Post, PostTranslationOptions)
translator.register(Comment, CommentTranslationOptions)
