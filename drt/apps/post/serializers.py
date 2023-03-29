from rest_framework import serializers
from models import Category, Post, Sponsorship, SponsorshipImage
from utils import get_download_url
import datetime


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsorship
        fields = ('text',)


class SponsorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorshipImage
        fields = ('image',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'guest', 'slug', 'job', 'title', 'image', 'url', 'duration', 'category', 'date', 'twitter')
        lookup_field = 'slug'


class PostSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Post
        lookup_field = 'slug'


class PostSerializerDetails(PostSerializerFull):
    download_url = serializers.SerializerMethodField(read_only=True)
    sponsorship = serializers.SerializerMethodField(read_only=True)
    sponsorship_image = serializers.SerializerMethodField(read_only=True)
    sponsorship_image_link = serializers.SerializerMethodField(read_only=True)
    sponsorship_image_text = serializers.SerializerMethodField(read_only=True)
    recommended = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_recommended(obj):
        return PostSerializer(Post.objects
                              .filter(date__gte=datetime.date(2016, 1, 1), status='p')
                              .exclude(id=obj.id).order_by('?')[:3], many=True).data

    @staticmethod
    def get_sponsorship(obj):
        return Sponsorship.objects.get(pk=obj.sponsor.id).text if obj.sponsor else ''

    @staticmethod
    def get_sponsorship_image(obj):
        return SponsorshipImage.objects.get(pk=obj.sponsorImage.id).image if obj.sponsorImage else ''

    @staticmethod
    def get_sponsorship_image_link(obj):
        return SponsorshipImage.objects.get(pk=obj.sponsorImage.id).redirectUrl if obj.sponsorImage else ''

    @staticmethod
    def get_sponsorship_image_text(obj):
        return SponsorshipImage.objects.get(pk=obj.sponsorImage.id).text if obj.sponsorImage else ''

    @staticmethod
    def get_download_url(obj):
        url = 'uploads/audio/' + obj.url.split('/')[-1]
        url = get_download_url('drt-resources', url)
        return url
