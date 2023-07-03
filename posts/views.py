from django.shortcuts import render
from rest_framework import generics


# Create your views here.
from posts.models import Post


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()


