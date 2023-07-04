from django.shortcuts import render
from rest_framework import generics


# Create your views here.
from rest_framework.generics import get_object_or_404

from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer


class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        try:
            queryset = Comment.objects.filter(post=self.kwargs['postId'])
            return queryset
        except Comment.DoesNotExist:
            return Comment.objects.none()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['postId'])
        serializer.save(commenter=self.request.user, post=post)
