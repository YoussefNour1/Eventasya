from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'


class Comment(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
