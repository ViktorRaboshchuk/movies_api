from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie, Review
from movies.serializers import MovieSerializer, MovieDetailSerializer, CreateReviewsSerializer


class MovieListView(APIView):

    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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

