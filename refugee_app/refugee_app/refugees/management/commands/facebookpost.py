from django.core.management.base import BaseCommand, CommandError
from refugees.models import Post, FacebookPost, Comment
import nltk
#from nltk.book import *
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
from nltk import FreqDist, bigrams
from collections import Counter
from django.conf import settings

class Command(BaseCommand):
    help = "some nltk stuff"

    def handle(self, *args, **options):
        

        posts = FacebookPost.objects.values_list('body', flat=True)
        my_list = []
        word_list = []
        for post in posts:
            my_list.append(post[0])
        
        for sentence in my_list:
            for word in sentence.split():
                word_list.append(word)
        
        # Skoða algengustu orðin:

        fdist = FreqDist(word_list)
        print(fdist.most_common(200))  

        # Leita að orðum sem eru meira en 15 stafir:

        V = set(word_list)
        long_words = [w for w in V if len(w) >15]
        sorted(long_words)
        #print(long_words)

        # prenta bara úr long_words
        #longwords = FreqDist(long_words)
        #print(longwords.most_common(200))

        #Leita að löngum orðum sem koma x oft fyrir (fdist þarf að vera skilgreint):

        #sorted(w for w in set(word_list) if len(w) >7 and fdist[w] >3)
        #print(sorted(w for w in set(word_list) if len(w) >7 and fdist[w] >3))

        #frekar svona: 

        freq_words = [w for w in (word_list) if len(w) >7 and fdist[w] >3]
        c = Counter(freq_words)

        print(c)

        for word, frequency in c.most_common(100):
        
            print('{} - {}'.format(word, frequency))


        #Til að búa til concordance:

        textList = Text(word_list)

        textList.concordance(settings.SEARCH_TERM)

        # Til að búa til collocations, 2 orð sem fara saman
        #textList.collocations()
        #print(textList.collocations)

        #similar:
        #textList.similar(settings.SEARCH_TERM)
        #print(textList)
    
        # Basic count
        #print(textList.count(settings.SEARCH_TERM))

        # Taka út það sem er hér að neðan: 