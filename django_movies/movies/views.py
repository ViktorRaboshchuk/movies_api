from django.db import models
from django.db.models import Avg
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ViewSet

from movies.models import Movie, Review, Actor
from movies.serializers import MovieSerializer, MovieDetailSerializer, CreateReviewsSerializer, \
    CreateRatingStarSerializer, ActorListSerializer, ActorDetailSerializer
from movies.service import get_client_ip, MovieFilter, PaginationMovies
from .permissions import IsSuperUser


class MovieListView(generics.ListAPIView):
    """List all movies"""
    serializer_class = MovieSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=(Avg('ratings__star'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """List movie by id"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewDestroy(generics.DestroyAPIView):
    """Remove review"""
    queryset = Review.objects.all()
    serializer_class = CreateReviewsSerializer
    permission_classes = [permissions.IsAdminUser]


class ReviewCreateView(generics.CreateAPIView):
    """Create review"""
    serializer_class = CreateReviewsSerializer
    permission_classes = [IsSuperUser]


class AddStarRatingView(generics.CreateAPIView):
    """Add rating star"""
    serializer_class = CreateRatingStarSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """ List of actors """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
    pagination_class = PaginationMovies


class ActorDetailView(generics.RetrieveAPIView):
    """ Show details about Actors and Directors"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
