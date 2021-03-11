from django.db import models
from django.db.models import Avg
from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie, Review, Actor
from movies.serializers import MovieSerializer, MovieDetailSerializer, CreateReviewsSerializer, \
    CreateRatingStarSerializer, ActorListSerializer, ActorDetailSerializer
from movies.service import get_client_ip


class MovieListView(APIView):

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=(Avg('ratings__star'))
        )
        serializers = MovieSerializer(movies, many=True)
        return Response(serializers.data)


class MovieDetailView(APIView):

    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializers = MovieDetailSerializer(movie)
        return Response(serializers.data)


class ReviewCreateView(APIView):

    def post(self, request):
        review = CreateReviewsSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):

    def post(self, request):
        serializer = CreateRatingStarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorsListView(generics.ListAPIView):
    """ List of actors """
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """ Show details about Actors and Directors"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer