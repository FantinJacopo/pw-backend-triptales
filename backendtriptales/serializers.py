from rest_framework import serializers
from .models import User, Comment, Badge, UserBadge, PostLike, TripGroup, Post

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'profile_image', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data.get('name', ''),
            password=validated_data['password'],
            profile_image=validated_data.get('profile_image', None)
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'profile_image', 'registration_date']

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url') and request:
            return request.build_absolute_uri(obj.profile_image.url)
        return None


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

class TripGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripGroup
        fields = ['id', 'group_name', 'group_image', 'description', 'invite_code', 'created_at']
        read_only_fields = ['invite_code']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'trip_group', 'image', 'smart_caption', 'latitude',
                  'longitude', 'created_at', 'ocr_text', 'object_tags']
        read_only_fields = ['user', 'created_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['trip_group', 'image', 'smart_caption']
