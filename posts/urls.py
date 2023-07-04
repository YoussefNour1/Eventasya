from django.urls import path
from . import views
urlpatterns = [
    path('', views.PostListCreate.as_view(), name='posts-list-create'),
    path('<int:postId>/comments/', views.CommentListCreate.as_view(), name='post-details'),
]