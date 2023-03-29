from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed
from post.models import Post
from datetime import datetime
from models import PodcastFeed
audio_path = 'https://drt-resources.s3.amazonaws.com/uploads/audio/'


class iTunesPodcastFeedGenerator(Rss201rev2Feed):
    mime_type = "application/xml"

    def rss_attributes(self):
        return {u"version": self._version,
                u"xmlns:atom": u"http://www.w3.org/2005/Atom",
                u'xmlns:itunes': u"http://www.itunes.com/dtds/podcast-1.0.dtd",
                u'xmlns:content': u"http://purl.org/rss/1.0/modules/content/",
                u'xmlns:wfw': u"http://wellformedweb.org/CommentAPI/",
                u'xmlns:dc': u"http://purl.org/dc/elements/1.1/",
                u'xmlns:sy': u"http://purl.org/rss/1.0/modules/syndication/",
                u'xmlns:slash': u"http://purl.org/rss/1.0/modules/slash/", }

    def add_root_elements(self, handler):
        super(iTunesPodcastFeedGenerator, self).add_root_elements(handler)
        handler.addQuickElement(u'itunes:subtitle', self.feed['subtitle'])
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:summary', self.feed['iTunes_summary'])
        handler.addQuickElement(u'itunes:explicit', self.feed['iTunes_explicit'])
        handler.startElement(u"itunes:owner", {})
        handler.addQuickElement(u'itunes:name', self.feed['author_name'])
        handler.addQuickElement(u'itunes:email', self.feed['iTunes_author_email'])
        handler.endElement(u"itunes:owner",)
        handler.addQuickElement(u'itunes:image', '', self.feed['iTunes_image'])
        handler.addQuickElement(u"itunes:category", '', {'text': 'Technology'})
        handler.startElement(u"itunes:category", {'text': 'Business'})
        handler.addQuickElement(u"itunes:category", '', {'text': 'Management & Marketing'})
        handler.endElement(u"itunes:category", )
        handler.startElement(u"itunes:category", {'text': 'Arts'})
        handler.addQuickElement(u"itunes:category", '', {'text': 'Design'})
        handler.endElement(u"itunes:category", )

    def add_item_elements(self,  handler, item):
        super(iTunesPodcastFeedGenerator, self).add_item_elements(handler, item)
        handler.addQuickElement(u'itunes:subtitle', item['summary'][0:250])
        handler.addQuickElement(u'itunes:summary', item['summary'])
        handler.addQuickElement(u'itunes:duration', item['duration'])
        handler.addQuickElement(u'itunes:explicit', item['explicit'])


class PostFeed(Feed):
    title = 'Dorm Room Tycoon - Business, Design and Technology Interviews'
    description = 'The podcast show that interviews the biggest names in business, design and tech.'
    author_name = 'William Channer'
    subtitle = 'Insightful interviews for hackers, product designers and startup founders. Learning from the world\'s most influential creators!'
    iTunes_summary = 'Interviews for designers, hackers, and startup founders.'
    iTunes_author_email = 'william.channer@gmail.com'
    iTunes_image_url = 'https://s3.amazonaws.com/drt-resources/uploads/images/logo.png'
    iTunes_explicit = 'yes'
    copyright = 'Copyright %s Dorm Room Tycoon'
    iTunes_image = dict()

    feed_type = iTunesPodcastFeedGenerator
    feed = PodcastFeed.objects.first()
    link = "/"
    if feed:
        title = feed.title
        description = feed.description
        author = feed.author
        subtitle = feed.subtitle
        iTunes_summary = feed.summary
        iTunes_author_email = feed.email
        iTunes_image_url = feed.image
        # iTunes_explicit = str(feed.explicit)
        copyright = feed.copyright % datetime.today().year
        iTunes_image['href'] = iTunes_image_url

    def feed_extra_kwargs(self, obj):
        extra = dict()
        extra['iTunes_summary'] = self.iTunes_summary
        extra['iTunes_author_email'] = self.iTunes_author_email
        extra['iTunes_image_url'] = self.iTunes_image_url
        extra['iTunes_explicit'] = self.iTunes_explicit
        extra['iTunes_image'] = self.iTunes_image

        return extra

    def items(self):
        return Post.objects.filter(status='p').order_by('-date', 'pk')

    def item_title(self, item):
        title = item.title
        if item.guest != "":
            title = title + ' with ' + item.guest
        if item.job != "":
            title = title + ', ' + item.job
        return title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return '/' + item.slug

    def item_extra_kwargs(self, item):
        return {'summary': item.description,
                'duration': item.duration,
                'explicit': 'yes'}

    def item_pubdate(self, item):
        return datetime.combine(item.date, datetime.min.time())

    def item_enclosure_url(self, item):
        print(item.url)
        return audio_path + item.url.split('/')[-1]

    def item_enclosure_length(self, item):
        return item.audio_length

    def item_enclosure_mime_type(self, item):
        return "audio/mp3"
