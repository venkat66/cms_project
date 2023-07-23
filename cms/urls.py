# cms/urls.py

from django.urls import path
from .views import (
    UserCreateAPIView,
    UserRetrieveUpdateDeleteAPIView,
    PostCreateAPIView,
    PostRetrieveUpdateDeleteAPIView,
    LikeCreateAPIView,
    LikeRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    # path('users/', UserCreateAPIView.as_view(), name='user-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDeleteAPIView.as_view(), name='user-retrieve-update-delete'),
    path('posts/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDeleteAPIView.as_view(), name='post-retrieve-update-delete'),
    path('likes/', LikeCreateAPIView.as_view(), name='like-create'),
    path('likes/<int:pk>/', LikeRetrieveUpdateDeleteAPIView.as_view(), name='like-retrieve-update-delete'),
]
