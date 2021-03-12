from django.db import models
from django.db.models import Avg
from django.shortcuts import render
from rest_framework import generics, permissions
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend

from movies.models import Movie, Review, Actor
from movies.serializers import MovieSerializer, MovieDetailSerializer, CreateReviewsSerializer, \
    CreateRatingStarSerializer, ActorListSerializer, ActorDetailSerializer
from movies.service import get_client_ip, MovieFilter, PaginationMovies


class MovieListView(generics.ListAPIView):

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

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):

    serializer_class = CreateReviewsSerializer


class AddStarRatingView(generics.CreateAPIView):
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
