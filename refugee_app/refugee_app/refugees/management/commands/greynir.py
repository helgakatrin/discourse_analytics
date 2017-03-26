from django.core.management.base import BaseCommand, CommandError
from refugees.models import Post, FacebookPost, Comment, WordCategory, CategoryType
import nltk
#from nltk.book import *
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
from nltk import FreqDist, bigrams
from collections import Counter
from django.conf import settings
import requests
import time

class Command(BaseCommand):
    help = "HTTP POST to the Greynir API"

    def handle(self, *args, **options):
        #comments = ' '.join(Comment.objects.values_list('body', flat=True))

        
        for comment in Comment.objects.filter(body_stemmed__isnull=True).prefetch_related('word_category'):

            print('############### Færsla hefst ############')
            print(comment.body)
            print('############### Færsla endar ############')
            print('*************** Greining hefst **********')
            payload = {'text': comment.body}
            res = requests.post('https://greynir.is/postag.api/v1', data=payload)
            print(res.text)
            print('*************** Greining endar **********')
            data = res.json()
            for result in data['result']:
                stem_list = []
                word_bank = []
                word_category_list = []
                for sentence in result:
                    keys = [k for k in sentence.keys()]
                    if set(['s']).issubset(set(keys)):
                        print(sentence['s'])
                        stem_list.append(sentence['s'])
                        if 'c' in keys:
                            if not sentence['c'] in ['st', 'fn', 'nhm', 'abfn', 'fs', 'ao', 'pfn']:
                                word_bank.append(sentence['s'])

                comment.body_stemmed = ' '.join(stem_list)
                comment.save()

                for word in word_bank:
                    wc, created = WordCategory.objects.update_or_create(word=word)
                    #word_category_list.append(wc)
                    comment.word_category.add(wc)
