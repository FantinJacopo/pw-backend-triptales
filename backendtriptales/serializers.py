from rest_framework import serializers
from .models import Comment, Badge, UserBadge, PostLike

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'
