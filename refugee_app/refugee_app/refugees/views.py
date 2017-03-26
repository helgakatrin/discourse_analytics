from django.views.decorators.csrf import csrf_exempt
from refugees.models import Post, FacebookPost, Comment
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.http import Http404
import json
from nltk import FreqDist, bigrams
from collections import Counter
import requests

def bubbles(request):
    return render(request, 'refugees/bubbles.html')

@csrf_exempt
def api_post(request):
    posts = Comment.objects.values_list('body', flat=True)

    word_list = []
    result = []
    for post in posts:
        if post:
            for item in post.split():
                word_list.append(item)
    
    
    
    fdist = FreqDist(word_list)


    freq_words = [w for w in (word_list) if len(w) >7 and fdist[w] >3]
    c = Counter(freq_words)

    for word, frequency in c.most_common(100):

        #print('{} - {}'.format(word, frequency))
        result.append({'word': word, 'frequency': frequency, 'group': 'post'})
    
    response = JsonResponse({'result': result})

    return response