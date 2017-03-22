from django.contrib import admin
from .models import Post, Comment, FacebookPost

class PostAdmin(admin.ModelAdmin):
    list_display = ['body']
    search_fields =  ['body']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['body']
    search_fields =  ['body']

class FacebookPostAdmin(admin.ModelAdmin):
    list_display = ['body']
    search_fields =  ['body']

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FacebookPost, FacebookPostAdmin)
