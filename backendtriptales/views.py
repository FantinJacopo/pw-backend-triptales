from django.db import models
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

from .badge_service import BadgeService
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

        # ===== BADGE CHECKS =====
        user_comment_count = Comment.objects.filter(user=self.request.user).count()

        # Check first comment
        if user_comment_count == 1:
            BadgeService.check_and_assign_badges(self.request.user, 'first_comment')

        # Check comment count milestone
        BadgeService.check_and_assign_badges(self.request.user, 'comment_count', count=user_comment_count)
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
        post = serializer.save(
            user=self.request.user,
            latitude=latitude,
            longitude=longitude
        )

        # ===== BADGE CHECKS =====
        user_post_count = Post.objects.filter(user=self.request.user).count()

        # Check first post
        if user_post_count == 1:
            BadgeService.check_and_assign_badges(self.request.user, 'first_post')

        # Check post count milestone
        BadgeService.check_and_assign_badges(self.request.user, 'post_count', count=user_post_count)

        # Check location badge
        if post.latitude and post.longitude:
            BadgeService.check_and_assign_badges(self.request.user, 'first_location')

        # Check AI usage badges
        if post.ocr_text or (post.object_tags and len(post.object_tags) > 0):
            BadgeService.check_and_assign_badges(self.request.user, 'first_ai')

            # Count AI posts for advanced badge
            ai_posts_count = Post.objects.filter(
                user=self.request.user
            ).exclude(ocr_text='').exclude(object_tags=[]).count()

            BadgeService.check_and_assign_badges(self.request.user, 'ai_count', count=ai_posts_count)
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
class UserBadgesView(APIView):
    """
    Ottiene i badge dell'utente corrente
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # IMPORTANTE: select_related per evitare query multiple
            user_badges = UserBadge.objects.filter(user=request.user).select_related('badge').order_by('-assigned_at')
            serializer = UserBadgeSerializer(user_badges, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Errore nel caricamento badge utente corrente: {e}")
            return Response(
                {"error": "Errore nel caricamento dei badge"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class UserBadgesByIdView(APIView):
    """
    Ottiene i badge di un utente specifico per ID
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = get_object_or_404(User, id=user_id)
            # IMPORTANTE: select_related per evitare query multiple
            user_badges = UserBadge.objects.filter(user=user).select_related('badge').order_by('-assigned_at')
            serializer = UserBadgeSerializer(user_badges, many=True, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "Utente non trovato"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Errore nel caricamento badge utente {user_id}: {e}")
            return Response(
                {"error": "Errore nel caricamento dei badge"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class CheckAndAssignBadgesView(APIView):
    """
    Vista per verificare e assegnare badge mancanti all'utente corrente
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        assigned_badges = []

        try:
            # Verifica badge "Fondatore"
            if TripGroup.objects.filter(creator=user).exists():
                founder_badge = Badge.objects.get(name="Fondatore")
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=founder_badge
                )
                if created:
                    assigned_badges.append("Fondatore")

            # Verifica badge "Primo Post"
            user_posts = Post.objects.filter(user=user)
            if user_posts.exists():
                first_post_badge = Badge.objects.get(name="Primo Post")
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=first_post_badge
                )
                if created:
                    assigned_badges.append("Primo Post")

            # Verifica badge "Fabrizio Corona" (10 post)
            if user_posts.count() >= 10:
                photo_badge = Badge.objects.get(name="Fabrizio Corona")
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=photo_badge
                )
                if created:
                    assigned_badges.append("Fabrizio Corona")

            # Verifica badge "Primo Commento"
            user_comments = Comment.objects.filter(user=user)
            if user_comments.exists():
                first_comment_badge = Badge.objects.get(name="Primo Commento")
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=first_comment_badge
                )
                if created:
                    assigned_badges.append("Primo Commento")

            # Verifica badge "Kanye West" (20 commenti)
            if user_comments.count() >= 20:
                comment_badge = Badge.objects.get(name="Kanye West")
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=comment_badge
                )
                if created:
                    assigned_badges.append("Kanye West")

            # Verifica badge "PLC" (5 post con posizione)
            location_posts = Post.objects.filter(
                user=user,
                latitude__isnull=False,
                longitude__isnull=False
            )
            if location_posts.count() >= 5:
                location_badge = Badge.objects.get(name="PLC")
                user_badge, created = UserBadge.objects.get_or_create(
                    user=user,
                    badge=location_badge
                )
                if created:
                    assigned_badges.append("PLC")

            return Response({
                "status": "success",
                "assigned_badges": assigned_badges,
                "message": f"Assegnati {len(assigned_badges)} nuovi badge!" if assigned_badges else "Nessun nuovo badge da assegnare"
            })

        except Badge.DoesNotExist as e:
            return Response({
                "status": "error",
                "message": f"Badge non trovato: {str(e)}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GroupLikesLeaderboardView(APIView):
    """
    Vista per ottenere la classifica degli utenti con più like in un gruppo specifico
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            # Verifica che il gruppo esista e che l'utente sia membro
            group = get_object_or_404(TripGroup, id=group_id)

            # Verifica che l'utente sia membro del gruppo
            if not GroupMembership.objects.filter(group=group, user=request.user).exists():
                return Response(
                    {"error": "Non sei membro di questo gruppo"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Query per ottenere la classifica dei like nel gruppo
            # Conta i like ricevuti dai post di ogni utente in questo gruppo
            leaderboard_data = (
                User.objects
                .filter(post__trip_group=group)  # Utenti che hanno postato in questo gruppo
                .annotate(
                    total_likes=models.Count('post__likes', distinct=True),
                    posts_count=models.Count('post', distinct=True)
                )
                .filter(total_likes__gt=0)  # Solo utenti con almeno un like
                .order_by('-total_likes', '-posts_count')  # Ordina per like decrescenti, poi per numero post
                [:10]  # Top 10
            )

            # Serializza i dati della classifica
            leaderboard = []
            for position, user in enumerate(leaderboard_data, 1):
                user_data = {
                    'position': position,
                    'user_id': user.id,
                    'user_name': user.name,
                    'user_profile_image': request.build_absolute_uri(
                        user.profile_image.url) if user.profile_image else None,
                    'total_likes': user.total_likes,
                    'posts_count': user.posts_count,
                    'is_current_user': user.id == request.user.id
                }
                leaderboard.append(user_data)

            # Trova la posizione dell'utente corrente se non è nella top 10
            current_user_position = None
            if request.user.id not in [user['user_id'] for user in leaderboard]:
                try:
                    current_user_stats = (
                        User.objects
                        .filter(id=request.user.id, post__trip_group=group)
                        .annotate(
                            total_likes=models.Count('post__likes', distinct=True),
                            posts_count=models.Count('post', distinct=True)
                        )
                        .first()
                    )

                    if current_user_stats and current_user_stats.total_likes > 0:
                        # Conta quanti utenti hanno più like dell'utente corrente
                        users_above = (
                            User.objects
                            .filter(post__trip_group=group)
                            .annotate(total_likes=models.Count('post__likes', distinct=True))
                            .filter(total_likes__gt=current_user_stats.total_likes)
                            .count()
                        )

                        current_user_position = {
                            'position': users_above + 1,
                            'user_id': request.user.id,
                            'user_name': request.user.name,
                            'user_profile_image': request.build_absolute_uri(
                                request.user.profile_image.url) if request.user.profile_image else None,
                            'total_likes': current_user_stats.total_likes,
                            'posts_count': current_user_stats.posts_count,
                            'is_current_user': True
                        }
                except Exception as e:
                    print(f"Errore nel calcolo posizione utente corrente: {e}")

            return Response({
                'group_id': group_id,
                'group_name': group.group_name,
                'leaderboard': leaderboard,
                'current_user_position': current_user_position,
                'total_participants': User.objects.filter(post__trip_group=group).distinct().count()
            })

        except Exception as e:
            print(f"Errore nella classifica like del gruppo {group_id}: {e}")
            return Response(
                {"error": "Errore nel caricamento della classifica"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GroupLikesLeaderboardView(APIView):
    """
    Vista per ottenere la classifica degli utenti con più like in un gruppo specifico
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            # Verifica che il gruppo esista e che l'utente sia membro
            group = get_object_or_404(TripGroup, id=group_id)

            # Verifica che l'utente sia membro del gruppo
            if not GroupMembership.objects.filter(group=group, user=request.user).exists():
                return Response(
                    {"error": "Non sei membro di questo gruppo"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Query per ottenere la classifica dei like nel gruppo
            # Conta i like ricevuti dai post di ogni utente in questo gruppo
            leaderboard_data = (
                User.objects
                .filter(post__trip_group=group)  # Utenti che hanno postato in questo gruppo
                .annotate(
                    total_likes=models.Count('post__likes', distinct=True),
                    posts_count=models.Count('post', distinct=True)
                )
                .filter(total_likes__gt=0)  # Solo utenti con almeno un like
                .order_by('-total_likes', '-posts_count')  # Ordina per like decrescenti, poi per numero post
                [:10]  # Top 10
            )

            # Serializza i dati della classifica
            leaderboard = []
            for position, user in enumerate(leaderboard_data, 1):
                user_data = {
                    'position': position,
                    'user_id': user.id,
                    'user_name': user.name,
                    'user_profile_image': request.build_absolute_uri(
                        user.profile_image.url) if user.profile_image else None,
                    'total_likes': user.total_likes,
                    'posts_count': user.posts_count,
                    'is_current_user': user.id == request.user.id
                }
                leaderboard.append(user_data)

            # Trova la posizione dell'utente corrente se non è nella top 10
            current_user_position = None
            if request.user.id not in [user['user_id'] for user in leaderboard]:
                try:
                    current_user_stats = (
                        User.objects
                        .filter(id=request.user.id, post__trip_group=group)
                        .annotate(
                            total_likes=models.Count('post__likes', distinct=True),
                            posts_count=models.Count('post', distinct=True)
                        )
                        .first()
                    )

                    if current_user_stats and current_user_stats.total_likes > 0:
                        # Conta quanti utenti hanno più like dell'utente corrente
                        users_above = (
                            User.objects
                            .filter(post__trip_group=group)
                            .annotate(total_likes=models.Count('post__likes', distinct=True))
                            .filter(total_likes__gt=current_user_stats.total_likes)
                            .count()
                        )

                        current_user_position = {
                            'position': users_above + 1,
                            'user_id': request.user.id,
                            'user_name': request.user.name,
                            'user_profile_image': request.build_absolute_uri(
                                request.user.profile_image.url) if request.user.profile_image else None,
                            'total_likes': current_user_stats.total_likes,
                            'posts_count': current_user_stats.posts_count,
                            'is_current_user': True
                        }
                except Exception as e:
                    print(f"Errore nel calcolo posizione utente corrente: {e}")

            return Response({
                'group_id': group_id,
                'group_name': group.group_name,
                'leaderboard': leaderboard,
                'current_user_position': current_user_position,
                'total_participants': User.objects.filter(post__trip_group=group).distinct().count()
            })

        except Exception as e:
            print(f"Errore nella classifica like del gruppo {group_id}: {e}")
            return Response(
                {"error": "Errore nel caricamento della classifica"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )