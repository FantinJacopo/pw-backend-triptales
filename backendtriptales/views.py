from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Comment, Badge, UserBadge, PostLike, User, TripGroup, Post
from .serializers import CommentSerializer, BadgeSerializer, UserBadgeSerializer, PostLikeSerializer, \
    UserRegistrationSerializer, TripGroupSerializer, PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class UserBadgeViewSet(viewsets.ModelViewSet):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer

class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TripGroupViewSet(viewsets.ModelViewSet):
    queryset = TripGroup.objects.all()
    serializer_class = TripGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        group = serializer.save()
        group.member_set.create(user=self.request.user, role='creator')
        return group

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Mostra solo i post nei gruppi in cui l'utente è membro
        return Post.objects.filter(user=self.request.user)