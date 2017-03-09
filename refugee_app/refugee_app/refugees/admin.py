from django.contrib import admin
from .models import Post, Comment, FacebookPost

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class FacebookPostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FacebookPost, FacebookPostAdmin)
