from django.contrib import admin
from models import Post, Category, Sponsorship, SponsorshipImage
from ordered_model.admin import OrderedModelAdmin
from datetime import datetime


def make_published(modeladmin, request, queryset):
    queryset.update(status='p', date=datetime.now())
make_published.short_description = "Mark selected as published"


def push_to_top(modeladmin, request, queryset):
    for post in queryset:
        post.top()
push_to_top.short_description = "Move to top"


def push_to_bottom(modeladmin, request, queryset):
    for post in queryset:
        post.bottom()
push_to_bottom.short_description = "Move to bottom"


def create_action_sponsor(sponsor):
    def action(modeladmin, request, queryset):
        queryset.update(sponsor=sponsor)

    name = "mark_%s" % (sponsor,)
    return name, (action, name, "Change sponsor to %s" % (sponsor,))


def create_action_sponsor_image(sponsor):
    def action(modeladmin, request, queryset):
        queryset.update(sponsorImage=sponsor)

    name = "mark_%s" % (sponsor,)
    return name, (action, name, "Change sponsor image to %s" % (sponsor,))


class PostAdmin(OrderedModelAdmin):
    fields = ('guest', 'slug', 'job', 'jobUrl', 'title', 'description', 'quote', 'about', 'transcript', 'image', 'url', 'duration',
              'twitter', 'education', 'educationUrl', 'app', 'appUrl', 'book', 'bookUrl', 'roleModel', 'roleModelUrl',
              'sponsor', 'sponsorImage', 'category', 'popular', 'featured', 'status', 'date')
    list_display = ('guest', 'title', 'sponsor', 'sponsorImage', 'category', 'date', 'popular', 'featured', 'status', 'move_up_down_links')
    list_filter = ('category', 'date', 'popular', 'featured', 'status', 'sponsor', 'sponsorImage')
    actions = [push_to_top, push_to_bottom]
    # save_as = True

    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request).copy()
        actions.update(dict(create_action_sponsor(sponsor) for sponsor in Sponsorship.objects.all()))
        actions.update(dict(create_action_sponsor_image(sponsor) for sponsor in SponsorshipImage.objects.all()))
        return actions


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'order', 'default',)


class SponsorAdmin(admin.ModelAdmin):
    pass


class SponsorImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Sponsorship, SponsorAdmin)
admin.site.register(SponsorshipImage, SponsorImageAdmin)
