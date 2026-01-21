from django.urls import path
from book import views

urlspatterns = [
    path('create/',views.BookCreatedView.as_view(),name='create'),
    path('list/',views.BookListView.as_view(),name='list'),
    path('deatil/',views.BookDetailView.as_view(),name='detail'),
    path('update/<int:pk>/',views.BookUpdateView.as_view(),name='update'),
    path('delete/<int:pk>/',views.BookDeleteView.as_view(),name='delete'),  
]
    