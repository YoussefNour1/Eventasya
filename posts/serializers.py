from rest_framework import serializers

from posts.models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    commenter_email = serializers.CharField(read_only=True, source='commenter.email')
    commenter_name = serializers.CharField(read_only=True, source='commenter.name')
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post', 'commenter', ]
