from django.contrib import admin
from models import PodcastFeed


class PodcastFeedAdmin(admin.ModelAdmin):
    pass


admin.site.register(PodcastFeed, PodcastFeedAdmin)
