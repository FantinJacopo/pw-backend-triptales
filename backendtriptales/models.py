from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    profile_image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username obbligatorio per AbstractUser

    def __str__(self):
        return self.name


class TripGroup(models.Model):
    group_name = models.CharField(max_length=100)
    group_image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    invite_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.group_name


class Member(models.Model):
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('member', 'Member')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_group = models.ForeignKey(TripGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} in {self.trip_group.group_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_group = models.ForeignKey(TripGroup, on_delete=models.CASCADE)
    image_url = models.URLField()
    smart_caption = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    ocr_text = models.TextField(blank=True)
    object_tags = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Post by {self.user.name} in {self.trip_group.group_name}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.name} on Post {self.post.id}"


class Badge(models.Model):
    name = models.CharField(max_length=50)
    badge_image_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'badge')  # evita duplicati

    def __str__(self):
        return f"{self.user.name} has badge {self.badge.name}"


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')  # evita duplicati

    def __str__(self):
        return f"{self.user.name} liked Post {self.post.id}"
