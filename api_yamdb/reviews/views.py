from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from users.permissions import (IsAdminOrReadOnly,
                               IsAuthorModeratorAdminSuperuser)

from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilters
from .mixins import ListCreateDestroyMixin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewsSerializer,
                          SafeMethodTitleSerializer, TitleSerializer)


class AbstractViewSet(ListCreateDestroyMixin):
    serializer_class = ...
    queryset = ...
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    class Meta:
        abstract = True


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthorModeratorAdminSuperuser,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        queryset = Comment.objects.filter(
            review_id=self.kwargs['review_id'])
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthorModeratorAdminSuperuser,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.review.all()

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer = ReviewsSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            if title.review.filter(author=self.request.user).exists():

                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save(author=self.request.user, title=title)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GenreViewSet(AbstractViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class CategoryViewSet(AbstractViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('review__score'))
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TitleFilters

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return SafeMethodTitleSerializer
        return TitleSerializer
