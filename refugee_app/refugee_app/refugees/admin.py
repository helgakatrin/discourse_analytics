from django.contrib import admin
from .models import Post, Comment, FacebookPost, FBAuthor

class AuthorCommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'posted', 'url']

class CommentAdmin(admin.ModelAdmin):
    pass

class FacebookPostAdmin(admin.ModelAdmin):
    pass

class FBAuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'fb_id']
    inlines = [AuthorCommentInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FacebookPost, FacebookPostAdmin)
admin.site.register(FBAuthor, FBAuthorAdmin)
