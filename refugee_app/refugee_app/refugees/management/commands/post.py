from django.core.management.base import BaseCommand, CommandError
from refugees.models import Post, FacebookPost, Comment
import nltk
#from nltk.book import *
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
from nltk import FreqDist, bigrams
from collections import Counter
from django.conf import settings
import csv
from datetime import datetime

class Command(BaseCommand):
    help = "some nltk stuff from visir.is and dv.is spider"

    def csv_export(self, word_list):
        with open('{}.csv'.format(datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S')), 'w+') as csv_file:
            fieldnames = ['word', 'frequency']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in word_list:
                writer.writerow({'word': data['word'], 'frequency': data['frequency']})

    def handle(self, *args, **options):
        

        posts = Post.objects.values_list('body', flat=True)
        my_list = []
        word_list = []

        for post in posts:
            words_in_post = post.split()
            for word in words_in_post:
                word_list.append(word)            

        # Skoða algengustu orðin:

        fdist = FreqDist(word_list)
        #print(fdist.most_common(200))  

        # Leita að orðum sem eru meira en 15 stafir:

        V = set(word_list)
        long_words = [w for w in V if len(w) >15]
        sorted(long_words)
        #print(long_words)

        #Leita að löngum orðum sem koma x oft fyrir (fdist þarf að vera skilgreint):

        #sorted(w for w in set(word_list) if len(w) >7 and fdist[w] >30)
        #print(sorted(w for w in set(word_list) if len(w) >7 and fdist[w] >30))

        #gera það frekar svona, þá fæ ég fjöldann með: 
        freq_words = [w for w in (word_list) if len(w) >7 and fdist[w] >3]
        c = Counter(freq_words)

        #print(c)
        data = [{'word': word, 'frequency': frequency} for word, frequency in c.most_common(200)]
        self.csv_export(data)

        for word, frequency in c.most_common(200):
        
            print('{} - {}'.format(word, frequency))

        #Til að búa til concordance:

        #textList = Text(word_list)

        #print(textList.collocations())

        #print(textList.concordance(settings.SEARCH_TERM))

        #similar:

        #print(textList.similar(settings.SEARCH_TERM))

    
        # Basic count

        #print(textList.count(settings.SEARCH_TERM))

