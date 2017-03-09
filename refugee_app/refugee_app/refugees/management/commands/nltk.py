from django.core.management.base import BaseCommand, CommandError
from refugees.models import *
import nltk

class Command(BaseCommand):
    help = "some nltk stuff"

    def handle(self, *args, **options):        
        posts = Post.objects.values_list('body')
        print(posts)