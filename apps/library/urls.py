from django.urls import path
from .views import AuthorListAPIView, AuthorDetailAPIView


app_name = 'library'

urlpatterns = [
    path('authors/', AuthorListAPIView.as_view(), name='authors_list'),
    path('authors/<uuid:pk>/', AuthorDetailAPIView.as_view(), name='authors_detail'),
]