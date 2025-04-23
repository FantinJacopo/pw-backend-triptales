from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, TripGroup, Member,
    Post, Comment, Badge,
    UserBadge, PostLike
)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('id', 'email', 'username', 'name', 'is_staff', 'registration_date')
    search_fields = ('email', 'username', 'name')
    ordering = ('-registration_date',)


@admin.register(TripGroup)
class TripGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'group_name', 'invite_code', 'created_at')
    search_fields = ('group_name', 'invite_code')
    list_filter = ('created_at',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip_group', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__email', 'trip_group__group_name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip_group', 'created_at', 'smart_caption')
    search_fields = ('smart_caption', 'ocr_text', 'user__name')
    list_filter = ('trip_group', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    search_fields = ('content', 'user__email')
    list_filter = ('created_at',)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('name',)


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'assigned_at')
    list_filter = ('assigned_at',)
    search_fields = ('user__email', 'badge__name')


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'liked_at')
    list_filter = ('liked_at',)
    search_fields = ('user__email',)
