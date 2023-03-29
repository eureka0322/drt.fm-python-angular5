from django.shortcuts import render
from django_user_agents.utils import get_user_agent
from post.models import Post
from post.utils import import_posts_from_dict
import xmltodict


def index(request):
    user_agent = get_user_agent(request)
    template = 'base.html'
    params = {
        'AppName': 'Dorm Room Tycoon',
        'BaseUrl': '/',
    }

    if user_agent.is_bot:
        template = 'base-bot.html'
        params['post'] = Post.objects.get(featured='True')

    return render(request, template, params)


def about(request):
    user_agent = get_user_agent(request)
    template = 'base.html'
    params = {
        'AppName': 'About | Dorm Room Tycoon',
        'BaseUrl': request.path,
    }

    if user_agent.is_bot:
        template = 'about-bot.html'

    return render(request, template, params)


def card(request):
    user_agent = get_user_agent(request)
    template = 'base.html'
    params = {
        'AppName': 'Dorm Room Tycoon',
        'BaseUrl': request.path,
    }

    if user_agent.is_bot:
        template = 'card-bot.html'
        slug = request.path.replace('/', '')
        params['post'] = Post.objects.get(slug=slug)

    return render(request, template, params)

# This imports the initial data from the old drt - use with caution


def test_import(request):
    import requests

    req = requests.get('https://drt.fm/rss')
    feed = xmltodict.parse(req.text)

    items = feed['rss']['channel']['item']
    posts = []
    for item in items:
        _post = import_posts_from_dict(item)
        # _post.save()
        posts.append(_post)

    return render(
        request, 'test-import.html', {
            'AppName': 'DRT Test Import',
            'rss': req.text,
            'items': posts
            }
        )

# This imports the initial data from the old drt - use with caution


def test_duration_import(request):
    import requests

    req = requests.get('https://drt.fm/rss')
    feed = xmltodict.parse(req.text)

    items = feed['rss']['channel']['item']
    posts = []
    for item in items:
        _post = import_posts_from_dict(item)

        post = Post.objects.filter(title=_post.title)[0]

        post.duration = _post.duration
        post.audio_length = _post.audio_length

        post.save()

        posts.append(post)

    return render(
        request, 'test-duration.html', {
            'AppName': 'DRT Test Import',
            'items': posts,
        }
    )
