from django.contrib import admin
from .models import Post, Comment, FacebookPost, FBAuthor, WordCategory, CategoryType

class AuthorCommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class CommentAdmin(admin.ModelAdmin):
    list_display = ['body', 'body_stemmed']
    search_fields =  ['body', 'id']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'posted', 'url', 'has_scraped_comments']
    search_fields =  ['url','body']

class WordCategoryAdmin(admin.ModelAdmin):
    list_display = ['word', 'category']
    search_fields =  ['word']

class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields =  ['title']

class FacebookPostAdmin(admin.ModelAdmin):
    pass

class FBAuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'fb_id']
    inlines = [AuthorCommentInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FacebookPost, FacebookPostAdmin)
admin.site.register(FBAuthor, FBAuthorAdmin)
admin.site.register(WordCategory, WordCategoryAdmin)
admin.site.register(CategoryType, CategoryTypeAdmin)
