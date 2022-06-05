from django.urls import path
from . import views

urlpatterns = [
    path('genre/', views.GenreView.as_view(), name='genre_view'),
    path('social-links/', views.SocialLinksView.as_view()),

    path('album/', views.AlbumView.as_view({'get': 'list'})),
    path('album/<int:pk>/', views.OneAlbumView.as_view({'get': 'list'})),

    path('artist/', views.ArtistView.as_view({'get': 'list'})),
    path('artist/<int:pk>/', views.OneArtistView.as_view({'get': 'list'})),

    path('rec/', views.ReccView.as_view({'get': 'list'})),
    path('rec-albums/', views.RecAlbumsView.as_view({'get': 'list'})),
    path('rec-artists/', views.RecArtistsView.as_view({'get': 'list'})),

    path('top/', views.TopView.as_view({'get': 'list'})),
    path('top-albums/', views.TopAlbumsView.as_view({'get': 'list'})),
    path('top-artists/', views.TopArtistsView.as_view({'get': 'list'})),

    path('track/', views.TrackUserView.as_view({'get': 'list'})),
    path('tracks/', views.TrackUserView.as_view({'get': 'get_tracks'})),

    path('stream-track/<int:pk>/', views.StreamingFileView.as_view()),

    path('playlist/', views.PlayListView.as_view({'get': 'list', 'post': 'create'})),
    path('playlist/<int:pk>/', views.PlayListView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),
    path('playlist-get/<int:pk>/', views.OnePlayListView.as_view({'get': 'list'})),
    path('playlist/<int:pk>/<int:pk1>/', views.OnePlayListView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),

    path('liked-songs/', views.LikedSongsView.as_view({'get': 'list'})),
    path('liked-songs/<int:pk>/', views.LikedSongsView.as_view({'patch': 'partial_update', 'delete': 'destroy'})),

]

