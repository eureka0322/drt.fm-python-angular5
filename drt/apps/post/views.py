from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import permission_classes, detail_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from serializers import PostSerializer, CategorySerializer, PostSerializerDetails
from models import Post, Category
from utils import get_download_url


@permission_classes((IsAuthenticatedOrReadOnly, ))
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'


class PostResultsSetPagination(LimitOffsetPagination):
    default_limit = 12


@permission_classes((IsAuthenticatedOrReadOnly, ))
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status='p')
    lookup_field = 'slug'
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter,)
    filter_fields = ('category__slug', 'popular', 'featured', )
    search_fields = ('guest', 'job', 'title',)
    pagination_class = PostResultsSetPagination

    def retrieve(self, request, slug=None):

        return Response(PostSerializerDetails(Post.objects.get(slug=slug)).data)

    @detail_route(methods=['GET'])
    def download_url(self, request, slug):
        post = Post.objects.get(slug=slug)
        url = 'uploads/audio/' + post.url.split('/')[-1]
        url = get_download_url('drt-resources', url)

        return Response(url)
