from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():  # Get all category
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movie(count=5):
    movies = Movie.objects.all().order_by('id')[:count]
    return {'last_movie': movies}
