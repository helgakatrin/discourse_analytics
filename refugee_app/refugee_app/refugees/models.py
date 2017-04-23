from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=254, default='')
    body = models.TextField(default='')
    posted = models.DateField(null=True)
    url = models.URLField()    
    has_scraped_comments = models.BooleanField(default=False)
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


class FBAuthor(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    fb_id = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name

class Comment(models.Model):    
    body = models.TextField()
    body_stemmed = models.TextField(null=True, blank=True)
    posted = models.DateField(null=True, blank=True)
    fb_created_time = models.DateTimeField(null=True, blank=True)
    author = models.CharField(max_length=254, blank=True)
    author_id = models.CharField(max_length=254, blank=True)
    post = models.ForeignKey(Post, null=True, blank=True)
    facebook_post = models.ForeignKey(FacebookPost, null=True, blank=True)
    screenshot = models.ImageField(upload_to='uploads/comments/', blank=True)
    fb_author = models.ForeignKey(FBAuthor, null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    fb_comment_id = models.CharField(max_length=256, unique=True, null=True, blank=True)
    word_category = models.ManyToManyField('WordCategory')

    def __str__(self):
        return self.body

# þetta á að vera inni
class WordCategory(models.Model):
    word = models.CharField(max_length=256)
    category = models.ForeignKey('CategoryType', null=True, blank=True)

    def __str__(self):
        return self.word

class CategoryType(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title