from urllib2 import urlopen
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime
from s3direct.fields import S3DirectField
from autoslug import AutoSlugField
from boto.s3.connection import S3Connection
from django.conf import settings
from ordered_model.models import OrderedModel


STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
)


class Category(models.Model):
    name = models.CharField("Name", max_length=45)
    color = models.CharField("Color", max_length=7, default="#000000")
    slug = AutoSlugField(populate_from="name", unique=True, editable=True)
    default = models.BooleanField("Default", default=False)
    order = models.IntegerField("Order", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Sponsorship(models.Model):
    title = models.CharField("Name", max_length=45)
    text = models.TextField("Text", default="")

    def __unicode__(self):
        return self.title


class SponsorshipImage(models.Model):
    title = models.CharField("Name", max_length=45)
    text = models.TextField("Text", default="", blank=True, null=True)
    redirectUrl = models.CharField("Redirect Url", max_length=255, blank=True, null=True)
    image = S3DirectField("Image", dest='image', default="", blank=True, null=True)

    def __unicode__(self):
        return self.title


class Post(OrderedModel):
    guest = models.CharField("Guest Name", max_length=255)
    slug = AutoSlugField(populate_from='guest', editable=True, unique=True)
    job = models.CharField("Company Title", max_length=255, blank=True, null=True)
    jobUrl = models.CharField("Company URL", max_length=255, blank=True, null=True)
    title = models.CharField("Interview Title", max_length=255, blank=True, null=True)
    description = models.TextField("Summary", default="", blank=True, null=True)
    quote = models.TextField("Quote", default="", blank=True, null=True)
    image = S3DirectField("Image", dest='image', default="", blank=True, null=True)
    url = S3DirectField("Audio", dest='audio', default="", blank=True, null=True)
    audio_length = models.IntegerField("Length in bytes", default=0, blank=True, null=True)
    duration = models.CharField("Duration hh:mm:ss", max_length=8, default="00:00:00", blank=True, null=True)
    twitter = models.CharField("Twitter Handle", max_length=255, blank=True, null=True)
    education = models.CharField("Education", max_length=255, blank=True, null=True)
    educationUrl = models.CharField("Education URL", max_length=255, blank=True, null=True)
    app = models.CharField("App Name", max_length=255, blank=True, null=True)
    appUrl = models.CharField("App URL", max_length=255, blank=True, null=True)
    book = models.CharField("Book Title", max_length=255, blank=True, null=True)
    bookUrl = models.CharField("Book URL", max_length=255, blank=True, null=True)
    roleModel = models.CharField("Role Model", max_length=255, blank=True, null=True)
    roleModelUrl = models.CharField("Role Model URL", max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, default=None, blank=True, null=True)
    date = models.DateField("Publish Date", default=datetime.now)
    about = models.TextField("About", default="", blank=True, null=True)
    transcript = models.TextField("Transcript", default="", blank=True, null=True)
    location = models.CharField("Location", max_length=255, blank=True, null=True)
    locationUrl = models.CharField("Location URL", max_length=255, blank=True, null=True)
    blog = models.CharField("Blog", max_length=255, blank=True, null=True)
    blogUrl = models.CharField("Blog URL", max_length=255, blank=True, null=True)
    popular = models.BooleanField("Popular", default=False)
    featured = models.BooleanField("Featured", default=False)
    published = models.BooleanField("Published", default=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='q')
    sponsor = models.ForeignKey("Sponsorship", blank=True, null=True)
    sponsorImage = models.ForeignKey("SponsorshipImage", blank=True, null=True)

    class Meta(OrderedModel.Meta):
        pass

    def __unicode__(self):
        return self.slug

    @staticmethod
    def get_absolute_url():
        return reverse('base-card')

    def get_file_meta(self):
        connection = S3Connection(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        filename = self.url.split('/')[-1]

        bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = bucket.lookup('uploads/audio/'+filename)
        return key

    @staticmethod
    def pre_save(sender, **kwargs):
        instance = kwargs.get('instance')
        file_meta = instance.get_file_meta()
        instance.audio_length = file_meta.size
        instance.image = instance.image.replace('s3.amazonaws.com/drt-resources', 'drt-resources.imgix.net')
        # instance.url = instance.url.replace('s3.amazonaws.com/drt-resources/uploads/audio', 'd2ikl1ia3vo2at.cloudfront.net')

    @staticmethod
    def post_save(sender, instance, created, *args, **kwargs):
        if created:
            instance.top()

    def save(self, *args, **kwargs):
        if self.featured:
            Post.objects.filter(featured=True, status='p').update(featured=False)

        super(Post, self).save(*args, **kwargs)

pre_save.connect(Post.pre_save, Post)
post_save.connect(Post.post_save, Post)
