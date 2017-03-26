from django.core.management.base import BaseCommand, CommandError
from refugees.models import Post, FacebookPost, Comment, FBAuthor
import time
import requests
from refugee_app.settings_local import FB_API_KEY
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Get facebook comments from news urls"
    

    def handle(self, *args, **options):
        fb_url = 'https://graph.facebook.com/'
        fb_url_comments = 'https://graph.facebook.com/{}/comments'

        payload = {'ids': ''}
        headers = {'Authorization': 'OAuth {}'.format(FB_API_KEY)}
        comment_list = Comment.objects.values_list('pk', flat=True)

        for post in Post.objects.exclude(has_scraped_comments=True):
            #if not Comment.objects.filter(post=post).exists():
            payload['ids'] = post.url
            res = requests.get(fb_url, params=payload, headers=headers)
            logger.info(res.url)
            
            try:
                fb_obj = res.json()[post.url]['og_object']['id']
            except KeyError as err:
                logger.error('URL not found in Facebook response: {}'.format(res.json()))
            else:
                res = requests.get(fb_url_comments.format(fb_obj), headers=headers)
                logger.info(res.json())

                try:
                    fb_data = res.json()['data']
                except KeyError:
                    logger.info('No data attribute found: {}'.format(res.json()))
                    continue
                else:
                    for item in res.json()['data']:
                        if item:
                            fb_author, created = FBAuthor.objects.update_or_create(
                                fb_id=item['from']['id'],
                                defaults={
                                    'name': item['from']['name']
                                })
                            if created:
                                logger.info('Author added: {}'.format(fb_author))
                            else:
                                logger.debug('Author updated: {}'.format(fb_author))

                            comment, created = Comment.objects.update_or_create(
                                fb_comment_id=item['id'],
                                defaults={
                                    'post': post,
                                    'body': item['message'],
                                    'fb_created_time': item['created_time'],
                                    'like_count': item['like_count'],
                                    'fb_author': fb_author
                                })
                            if created:
                                logger.info('Comment added: {}'.format(comment))
                            else:
                                logger.info('Comment updated: {}'.format(comment))
                        else:
                            logger.info('No item found: {}'.format(re.json()))
                    post.has_scraped_comments = True
                    post.save()
                    time.sleep(0.5)
