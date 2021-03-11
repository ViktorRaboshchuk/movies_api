
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from movies import views

urlpatterns = [
    path('movies/', views.MovieListView.as_view()),
    path('movie/<int:pk>/', views.MovieDetailView.as_view()),
    path('review/', views.ReviewCreateView.as_view()),
    path('rating/', views.AddStarRatingView.as_view()),
    path('actors/', views.ActorsListView.as_view()),
    path('actors/<int:pk>/', views.ActorDetailView.as_view()),
]


