from django.urls import path
from . import views

urlpatterns = [
    path('genre/', views.GenreView.as_view(), name='genre_view'),

    path('album/', views.AlbumView.as_view({'get': 'list', 'post': 'create'})),
    path('album/<int:pk>/', views.AlbumView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),

    # path('author-album/<int:pk>/', views.PublicAlbumView.as_view()),

    path('track/', views.TrackView.as_view({'get': 'list', 'post': 'create'})),
    path('track/<int:pk>/', views.TrackView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),

    path('stream-track/<int:pk>/', views.StreamingFileView.as_view()),

    path('playlist/', views.PlayListView.as_view({'get': 'list', 'post': 'create'})),
    path('playlist/<int:pk>/', views.PlayListView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),

]
