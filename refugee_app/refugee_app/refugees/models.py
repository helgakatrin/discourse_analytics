from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=254)
    body = models.TextField()
    posted = models.DateField(null=True)
    url = models.URLField()    

    def __str__(self):
        return self.title


class FacebookPost(models.Model):
    body = models.TextField(blank=True)
    posted = models.DateField(null=True, blank=True)
    url = models.URLField()    
    author = models.CharField(max_length=254, blank=True)
    author_id = models.CharField(max_length=254, blank=True)
    screenshot = models.ImageField(upload_to='uploads/facebook_posts/', blank=True)

    def __str__(self):
        return self.body


class Comment(models.Model):    
    body = models.TextField()
    posted = models.DateField(null=True, blank=True)    
    author = models.CharField(max_length=254, blank=True)
    author_id = models.CharField(max_length=254, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)
    facebook_post = models.ForeignKey(FacebookPost, null=True, blank=True)
    screenshot = models.ImageField(upload_to='uploads/comments/', blank=True)

    def __str__(self):
        return self.body