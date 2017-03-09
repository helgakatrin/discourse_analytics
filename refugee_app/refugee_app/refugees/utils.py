from django.db import models
from refugee_app.models import *


posts = Post.objects.values_list('body')
print(posts)