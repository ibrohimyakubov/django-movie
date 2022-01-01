from django.shortcuts import render
from django.views.generic import View, ListView, DetailView
from .models import *


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movies_list'
    template_name = 'movies/movies_list.html'


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'
