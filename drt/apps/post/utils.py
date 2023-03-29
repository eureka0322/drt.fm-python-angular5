from django.utils.dateparse import parse_date
from django.conf import settings
from dateutil import parser
from post.models import Post, Category
from boto.s3.connection import S3Connection


def get_download_url(bucket, path, https=True, expiry=315550000):

    connection = S3Connection(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    url = connection.generate_url(
        expires_in=long(expiry),
        method='GET',
        bucket=bucket,
        key=path,
        query_auth=True,
        force_http=(not https),
        response_headers={'response-content-disposition': 'attachment'}
    )

    return url


def __extract_from_url(item, post, param):
    item = item.replace('<a href="', '')
    item = item.replace('</a>', '')
    item = item.split('">')
    item_len = len(item)
    if item_len > 1:
        setattr(post, param, item[1])
        setattr(post, param + 'Url', item[0])
    elif item_len > 0:
        setattr(post, param, item[0])


def import_posts_from_dict(item):
    image_path = 'https://drt-resources.imgix.net/uploads/images/'
    audio_path = 'https://drt-resources.s3.amazonaws.com/uploads/audio/'
    ftr = [3600, 60, 1]

    post = Post()
    title = item['title'].split(' - ')
    post.guest = title[1]
    post.title = title[0]
    post.description = item['description']
    audio = item['enclosure']['@url']
    post.url = audio_path + audio.split('/')[-1]
    post.audio_length = item['enclosure']['@length']
    image = item['image']['@url']
    post.image = image_path + image.split('/')[-1]
    post.quote = item['quote']
    post.about = item['about']
    post.date = parser.parse(item['pubDate'])

    cat, created = Category.objects.get_or_create(
        name=item['category'][0]
    )

    post.category = cat

    if 'itunes:duration' in item:
        post.duration = item['itunes:duration']
    if 'twitter' in item:
        post.twitter = item['twitter']
    if 'education' in item:
        __extract_from_url(item['education'], post, 'education')
    if 'job' in item:
        __extract_from_url(item['job'], post, 'job')
    if 'model' in item:
        __extract_from_url(item['model'], post, 'roleModel')
    if 'app' in item:
        __extract_from_url(item['app'], post, 'app')
    if 'book' in item:
        __extract_from_url(item['book'], post, 'book')
    if 'location' in item:
        __extract_from_url(item['location'], post, 'location')
    if 'blog' in item:
        __extract_from_url(item['blog'], post, 'blog')

    return post
