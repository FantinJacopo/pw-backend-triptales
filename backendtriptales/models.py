import uuid
import os
from io import BytesIO
from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver

import qrcode
from qrcode.image.styledpil import StyledPilImage


class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    registration_date = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.name


class TripGroup(models.Model):
    group_name = models.CharField(max_length=100)
    group_image = models.ImageField(upload_to='groups/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    invite_code = models.CharField(max_length=5, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMembership', related_name='trip_groups')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()

        # Genera il QR code se non esiste
        if not self.qr_code:
            self.generate_qr_code()

        super().save(*args, **kwargs)

    def generate_invite_code(self):
        return str(uuid.uuid4())[:5]

    def generate_qr_code(self):
        # Genera il contenuto del QR code
        qr_data = f"{self.invite_code}"

        # Crea l'oggetto QRCode con le impostazioni corrette
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Genera l'immagine del QR code
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Salva l'immagine in memoria
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        buffer.seek(0)

        # Crea il nome del file
        qr_filename = f"qr_{self.invite_code}.png"

        # Salva il file nel campo ImageField
        self.qr_code.save(
            qr_filename,
            ContentFile(buffer.getvalue()),
            save=False
        )

    def is_creator(self, user):
        """Verifica se l'utente è il creatore del gruppo"""
        return self.creator == user

    def add_member(self, user):
        """Aggiunge un membro al gruppo se non è già presente"""
        membership, created = GroupMembership.objects.get_or_create(
            group=self,
            user=user,
            defaults={'joined_at': timezone.now()}
        )
        return membership, created

    def __str__(self):
        return self.group_name


# Tabella intermedia semplificata per tenere traccia della data di ingresso
class GroupMembership(models.Model):
    group = models.ForeignKey(TripGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.name} in {self.group.group_name}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip_group = models.ForeignKey(TripGroup, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True, default=None)
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
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.name} has badge {self.badge.name}"


class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.name} liked Post {self.post.id}"


# ============================
# SIGNALS PER ASSEGNAZIONE BADGE
# ============================

@receiver(post_save, sender=TripGroup)
def assign_founder_badge(sender, instance, created, **kwargs):
    """
    Assegna automaticamente il badge "Fondatore" quando un utente crea un gruppo
    """
    if created and instance.creator:
        try:
            # Cerca il badge "Fondatore"
            founder_badge = Badge.objects.get(name="Fondatore")

            # Assegna il badge all'utente se non ce l'ha già
            UserBadge.objects.get_or_create(
                user=instance.creator,
                badge=founder_badge,
                defaults={'assigned_at': timezone.now()}
            )
            print(f"Badge 'Fondatore' assegnato a {instance.creator.name}")
        except Badge.DoesNotExist:
            print("Badge 'Fondatore' non trovato nel database")


@receiver(post_save, sender=Post)
def assign_post_badges(sender, instance, created, **kwargs):
    """
    Assegna badge relativi ai post (es. "Primo Post", "Fabrizio Corona")
    """
    if created and instance.user:
        try:
            # Controlla se è il primo post dell'utente
            user_posts_count = Post.objects.filter(user=instance.user).count()

            if user_posts_count == 1:
                # Assegna badge "Primo Post"
                first_post_badge = Badge.objects.get(name="Primo Post")
                UserBadge.objects.get_or_create(
                    user=instance.user,
                    badge=first_post_badge,
                    defaults={'assigned_at': timezone.now()}
                )
                print(f"Badge 'Primo Post' assegnato a {instance.user.name}")

            # Badge "Fabrizio Corona" per chi ha postato 10 foto
            if user_posts_count == 10:
                photo_badge = Badge.objects.get(name="Fabrizio Corona")
                UserBadge.objects.get_or_create(
                    user=instance.user,
                    badge=photo_badge,
                    defaults={'assigned_at': timezone.now()}
                )
                print(f"Badge 'Fabrizio Corona' assegnato a {instance.user.name}")

        except Badge.DoesNotExist as e:
            print(f"Badge non trovato: {e}")


@receiver(post_save, sender=Comment)
def assign_comment_badges(sender, instance, created, **kwargs):
    """
    Assegna badge relativi ai commenti (es. "Primo Commento", "Kanye West")
    """
    if created and instance.user:
        try:
            # Controlla se è il primo commento dell'utente
            user_comments_count = Comment.objects.filter(user=instance.user).count()

            if user_comments_count == 1:
                # Assegna badge "Primo Commento"
                first_comment_badge = Badge.objects.get(name="Primo Commento")
                UserBadge.objects.get_or_create(
                    user=instance.user,
                    badge=first_comment_badge,
                    defaults={'assigned_at': timezone.now()}
                )
                print(f"Badge 'Primo Commento' assegnato a {instance.user.name}")

            # Badge "Kanye West" per chi ha fatto 20 commenti
            if user_comments_count == 20:
                comment_badge = Badge.objects.get(name="Kanye West")
                UserBadge.objects.get_or_create(
                    user=instance.user,
                    badge=comment_badge,
                    defaults={'assigned_at': timezone.now()}
                )
                print(f"Badge 'Kanye West' assegnato a {instance.user.name}")

        except Badge.DoesNotExist as e:
            print(f"Badge non trovato: {e}")


@receiver(post_save, sender=Post)
def assign_location_badge(sender, instance, created, **kwargs):
    """
    Assegna badge "PLC" per chi ha condiviso 5 post con posizione
    """
    if created and instance.user and instance.latitude and instance.longitude:
        try:
            # Conta i post con posizione dell'utente
            location_posts_count = Post.objects.filter(
                user=instance.user,
                latitude__isnull=False,
                longitude__isnull=False
            ).count()

            if location_posts_count == 5:
                location_badge = Badge.objects.get(name="PLC")
                UserBadge.objects.get_or_create(
                    user=instance.user,
                    badge=location_badge,
                    defaults={'assigned_at': timezone.now()}
                )
                print(f"Badge 'PLC' assegnato a {instance.user.name}")

        except Badge.DoesNotExist as e:
            print(f"Badge non trovato: {e}")