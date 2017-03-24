from django.core.management.base import BaseCommand, CommandError
from refugees.models import Post, FacebookPost, Comment


class Command(BaseCommand):
    help = "sql"

    def handle(self, *args, **options):

        posts = Post.objects.values_list('body', flat=True)
        my_list = []
        word_list = []
        for post in posts:
            my_list.append(post[0])
        
        for sentence in my_list:
            for word in sentence.split():
                word_list.append(word)      

        for p in Post.objects.raw('SELECT * FROM refugees_post'):
            print(p)
