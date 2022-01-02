from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView
from .models import *
from .forms import ReviewForm


class MoviesView(ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    context_object_name = 'movies_list'
    template_name = 'movies/movies_list.html'


class MovieDetailView(DetailView):
    model = Movie
    slug_field = 'url'


def add_comment(request, pk):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = Reviews()
            data.text = form.cleaned_data['text']
            data.email = form.cleaned_data['email']
            data.name = form.cleaned_data['name']
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            data.movie_id = pk
            data.save()
            messages.success(request, "Sizning kommentariyangiz qabul qilindi!")
            return HttpResponseRedirect(url)
    return redirect(url)
