from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.conf import settings

from .models import Comment, Badge, UserBadge, PostLike, User, TripGroup, Post
from .serializers import (
    CommentSerializer, BadgeSerializer, UserBadgeSerializer,
    PostLikeSerializer, UserRegistrationSerializer, TripGroupSerializer,
    PostSerializer, PostCreateSerializer, UserProfileSerializer
)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.all()

        # Filtra per post_id se presente nei query parameters
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)

        # Ordina i commenti per data di creazione (più recenti prima)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        # Assegna automaticamente l'utente loggato
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


# Resto delle views rimane uguale...
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
    parser_classes = [MultiPartParser, FormParser]

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
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        group = serializer.save()
        group.member_set.create(user=self.request.user, role='creator')
        return group

    @action(detail=False, methods=['get'])
    def my_groups(self, request):
        user = request.user
        groups = TripGroup.objects.filter(member__user=user)
        serializer = self.get_serializer(groups, many=True, context={'request': request})
        return Response(serializer.data)


class GroupPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        posts = Post.objects.filter(trip_group_id=group_id)
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -----------------------
# QR Code Management Views
# -----------------------

class GenerateQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            group = TripGroup.objects.get(id=group_id)
            if not group.qr_code:
                # Genera il QR code se non esiste
                group.qr_code = group.generate_qr_code()
                group.save()
            qr_code_url = f"{settings.MEDIA_URL}{group.qr_code}"
            return JsonResponse({"status": "success", "qr_code_url": qr_code_url})
        except TripGroup.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Gruppo non trovato"}, status=404)


class JoinGroupByQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qr_code = request.data.get("qr_code")
        if not qr_code:
            return JsonResponse({"status": "error", "message": "QR code non fornito"}, status=400)

        try:
            group = TripGroup.objects.get(invite_code=qr_code)
            # Aggiungi l'utente al gruppo
            group.member_set.create(user=request.user, role='member')
            return JsonResponse({"status": "success", "message": f"Unito al gruppo {group.group_name}"})
        except TripGroup.DoesNotExist:
            return JsonResponse({"status": "error", "message": "QR code non valido"}, status=404)


def join_group(request):
    qr_code = request.POST.get("qr_code")
    try:
        group = TripGroup.objects.get(qr_code=qr_code)
        # Logica per aggiungere l'utente al gruppo
        return JsonResponse({"status": "success", "message": f"Unito al gruppo {group.name}"})
    except TripGroup.DoesNotExist:
        return JsonResponse({"status": "error", "message": "QR Code non valido"}, status=404)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data)