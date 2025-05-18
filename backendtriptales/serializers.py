from rest_framework import serializers
from .models import User, Comment, Badge, UserBadge, PostLike, TripGroup, Post, GroupMembership


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
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'user_name', 'user_profile_image', 'content', 'created_at']
        read_only_fields = ['user', 'created_at', 'user_name', 'user_profile_image']

    def get_user_profile_image(self, obj):
        request = self.context.get('request')
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url') and request:
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class UserBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBadge
        fields = '__all__'

class PostLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'user_name', 'post', 'liked_at']
        read_only_fields = ['user', 'liked_at', 'user_name']

    def validate(self, attrs):
        # Verifica se l'utente ha già messo like a questo post
        user = self.context['request'].user
        post = attrs.get('post')

        if PostLike.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError({"error": "You have already liked this post"})

        return attrs

class TripGroupSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()
    group_image_url = serializers.SerializerMethodField()
    creator_name = serializers.CharField(source='creator.name', read_only=True)
    is_creator = serializers.SerializerMethodField()
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = TripGroup
        fields = ['id', 'group_name', 'group_image', 'group_image_url', 'description',
                  'invite_code', 'qr_code_url', 'creator', 'creator_name', 'is_creator',
                  'members_count', 'created_at']
        read_only_fields = ['invite_code', 'qr_code_url', 'creator', 'creator_name', 'is_creator', 'members_count']

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code and hasattr(obj.qr_code, 'url') and request:
            return request.build_absolute_uri(obj.qr_code.url)
        return None

    def get_group_image_url(self, obj):
        request = self.context.get('request')
        if obj.group_image and hasattr(obj.group_image, 'url') and request:
            return request.build_absolute_uri(obj.group_image.url)
        return None

    def get_is_creator(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_creator(request.user)
        return False

    def get_members_count(self, obj):
        return obj.members.count()

class PostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_profile_image = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user_id', 'user_name', 'user_profile_image', 'trip_group', 'image', 'image_url',
                  'smart_caption', 'latitude', 'longitude', 'created_at', 'ocr_text', 'object_tags',
                  'comments_count', 'likes_count']
        read_only_fields = ['user_id', 'user_name', 'user_profile_image', 'created_at', 'comments_count', 'likes_count']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url') and request:
            return request.build_absolute_uri(obj.image.url)
        return None

    def get_user_profile_image(self, obj):
        request = self.context.get('request')
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url') and request:
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['trip_group', 'image', 'smart_caption', 'latitude', 'longitude']

class GroupMembershipSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_profile_image = serializers.SerializerMethodField()

    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'user_name', 'user_email', 'user_profile_image', 'group', 'joined_at']
        read_only_fields = ['user_name', 'user_email', 'user_profile_image', 'joined_at']

    def get_user_profile_image(self, obj):
        request = self.context.get('request')
        if obj.user.profile_image and hasattr(obj.user.profile_image, 'url') and request:
            return request.build_absolute_uri(obj.user.profile_image.url)
        return None