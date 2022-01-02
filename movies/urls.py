from django.urls import path
from .views import MoviesView, MovieDetailView, add_comment

urlpatterns = [
    path('', MoviesView.as_view()),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', add_comment, name='add_review'),
]
