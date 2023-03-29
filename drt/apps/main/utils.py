from django.conf import settings
from rest_framework.renderers import JSONRenderer


def current_site_url():
    """Returns fully qualified URL (no trailing slash) for the current site."""
    from django.contrib.sites.models import Site
    if Site._meta.installed:
        current_site = Site.objects.get_current()
        return current_site
        # protocol = getattr(settings, 'SITE_PROTOCOL', 'http')
        # port = getattr(settings, 'SITE_PORT', '')
        # url = '%s://%s' % (protocol, current_site.domain)
        # if port:
        #     url += ':%s' % port
        # return url


class CustomJSONRenderer(JSONRenderer):
    """
    Override the render method of the django rest framework JSONRenderer to allow the following:
    * adding a resource_name root element to all GET requests formatted with JSON
    * reformatting paginated results to the following structure {meta: {}, resource_name: [{},{}]}

    NB: This solution requires a custom pagination serializer and an attribute of 'resource_name'
        defined in the serializer
    """


def render(self, data, accepted_media_type=None, renderer_context=None):
    response_data = {}

    #determine the resource name for this request - default to objects if not defined
    resource = getattr(renderer_context.get('view').get_serializer().Meta, 'resource_name', 'objects')

    #check if the results have been paginated
    if data.get('paginated_results'):
        #add the resource key and copy the results
        response_data['meta'] = data.get('meta')
        response_data[resource] = data.get('paginated_results')
    else:
        response_data[resource] = data

    #call super to render the response
    response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)

    return response