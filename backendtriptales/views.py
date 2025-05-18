from jsonschema import ValidationError
from rest_framework import status, viewsets, generics
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Comment, Badge, UserBadge, PostLike, User, TripGroup, Post, GroupMembership
from .serializers import (
    CommentSerializer, BadgeSerializer, UserBadgeSerializer,
    PostLikeSerializer, UserRegistrationSerializer, TripGroupSerializer,
    PostSerializer, PostCreateSerializer, UserProfileSerializer,
    GroupMembershipSerializer
)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user, context={"request": request})
        return Response(serializer.data)

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


class BadgeViewSet(viewsets.ModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer


class UserBadgeViewSet(viewsets.ModelViewSet):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer

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
        # Salva il gruppo con l'utente corrente come creator
        group = serializer.save(creator=self.request.user)

        # Aggiunge automaticamente il creator come membro
        GroupMembership.objects.create(group=group, user=self.request.user)

        return group

    @action(detail=False, methods=['get'])
    def my_groups(self, request):
        user = request.user

        # Trova tutti i gruppi dove l'utente è creator o membro
        groups = TripGroup.objects.filter(
            Q(creator=user) | Q(members=user)
        ).distinct()

        serializer = self.get_serializer(groups, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """
        Ottiene i membri di un gruppo specifico
        """
        try:
            group = self.get_object()

            # Ottieni tutte le membership per questo gruppo
            memberships = GroupMembership.objects.filter(group=group)

            # Serializza i dati con il serializer appropriato
            serializer = GroupMembershipSerializer(
                memberships,
                many=True,
                context={'request': request}
            )

            return Response(serializer.data)
        except TripGroup.DoesNotExist:
            return Response(
                {"error": "Gruppo non trovato"},
                status=status.HTTP_404_NOT_FOUND
            )


class GroupPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        posts = Post.objects.filter(trip_group_id=group_id).order_by('-created_at')
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
        return Post.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        # Estrai i dati del form incluse le coordinate
        latitude = self.request.data.get('latitude')
        longitude = self.request.data.get('longitude')

        # Converti le stringhe in float se presenti
        if latitude:
            try:
                latitude = float(latitude)
            except (ValueError, TypeError):
                latitude = None

        if longitude:
            try:
                longitude = float(longitude)
            except (ValueError, TypeError):
                longitude = None

        # Salva il post con l'utente corrente e le coordinate
        serializer.save(
            user=self.request.user,
            latitude=latitude,
            longitude=longitude
        )

class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = PostLike.objects.all()

        # Filtra per post_id se presente nei query parameters
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)

        # Filtra per user se l'endpoint è 'user'
        if self.action == 'user_likes':
            queryset = queryset.filter(user=self.request.user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def user_likes(self, request):
        """
        Ottiene tutti i like dell'utente corrente
        """
        likes = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def post_likes(self, request):
        """
        Ottiene tutti i like per un post specifico
        """
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response({"error": "post_id query parameter is required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"},
                            status=status.HTTP_404_NOT_FOUND)

        likes = post.likes.all()  # Assicurati che il related_name sia 'likes' nel modello
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data)

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
                group.generate_qr_code()
                group.save()
            qr_code_url = request.build_absolute_uri(group.qr_code.url)
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

            # Verifica se l'utente è già membro del gruppo
            membership, created = GroupMembership.objects.get_or_create(
                group=group,
                user=request.user,
                defaults={'joined_at': timezone.now()}
            )

            if created:
                return JsonResponse({
                    "status": "success",
                    "message": f"Unito al gruppo {group.group_name}"
                })
            else:
                return JsonResponse({
                    "status": "info",
                    "message": f"Sei già membro del gruppo {group.group_name}"
                })

        except TripGroup.DoesNotExist:
            return JsonResponse({"status": "error", "message": "QR code non valido"}, status=404)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data)