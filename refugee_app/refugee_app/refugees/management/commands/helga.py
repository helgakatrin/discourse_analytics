from django.core.management.base import BaseCommand, CommandError
from refugees.models import Post, FacebookPost, Comment
import nltk
#from nltk.book import *
from nltk.corpus import PlaintextCorpusReader
from nltk.text import Text
from nltk import FreqDist, bigrams


class Command(BaseCommand):
    help = "some nltk stuff"

    def handle(self, *args, **options):
        

        posts = list(FacebookPost.objects.values_list('body'))
        my_list = []
        word_list = []
        for post in posts:
            my_list.append(post[0])
        
        for sentence in my_list:
            for word in sentence.split():
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

        sorted(w for w in set(word_list) if len(w) >7 and fdist[w] >3)
        print(sorted(w for w in set(word_list) if len(w) >7 and fdist[w] >3))

        #Til að búa til concordance:

        textList = Text(word_list)

        #textList.concordance('hæli')
        #textList.concordance('hælisleitendur')
        #textList.concordance('hælisleitenda')

        #similar:

        #textList.similar('hæli')
        #textList.similar('hælisleitendur')
    
        # Basic count

        #textList.count("hælisleitandi") 
        #print(textList.count("hælisleitandi"))




        # Taka út það sem er hér að neðan: 

        #posts = Post.objects.values_list('body')
        """
        mitt_freq = FreqDist(listi)
        for post in posts:
            #for word in post['body'].split():
            results.append(nltk.word_tokenize(post['body'].split()))
        """     
        #print(results)
        
        # nltk 1.3 concordance = hvaða orð eru á undan og eftir ákveðnu orði        
        #results.concordance("orð")
        #results.similar("orð")        
        #fdist = FreqDist(results)
        #print(fdist.most_common(50))
        #print(results.dispersion_plot(['sigmundur']))
        #print(list(bigrams(results)))

