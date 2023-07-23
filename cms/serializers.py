from rest_framework import serializers
from .models import User, Post, Like

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    num_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_num_likes(self, obj):
        return obj.like_set.count()

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
