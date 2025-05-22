from .models import Badge, UserBadge, User, Post, Comment, TripGroup, GroupMembership
from django.db.models import Count


class BadgeService:
    @staticmethod
    def check_and_assign_badges(user, action_type, **kwargs):
        """Controlla e assegna badge basati sull'azione"""

        if action_type == 'first_post':
            BadgeService._assign_if_not_exists(user, 'Primo Post')

        elif action_type == 'post_count':
            post_count = kwargs.get('count', 0)
            if post_count >= 5:
                BadgeService._assign_if_not_exists(user, 'Fabrizio Corona')

        elif action_type == 'first_comment':
            BadgeService._assign_if_not_exists(user, 'Primo Commento')

        elif action_type == 'comment_count':
            comment_count = kwargs.get('count', 0)
            if comment_count >= 10:
                BadgeService._assign_if_not_exists(user, 'Kanye West')

        elif action_type == 'first_group':
            BadgeService._assign_if_not_exists(user, 'Fondatore')

        elif action_type == 'group_membership':
            group_count = kwargs.get('count', 0)
            if group_count >= 3:
                BadgeService._assign_if_not_exists(user, 'Nico B')

        elif action_type == 'first_location':
            BadgeService._assign_if_not_exists(user, 'Esploratore')

        elif action_type == 'first_ai':
            BadgeService._assign_if_not_exists(user, 'm-niky')

        elif action_type == 'ai_count':
            ai_count = kwargs.get('count', 0)
            if ai_count >= 10:
                BadgeService._assign_if_not_exists(user, 'Cucippo')

    @staticmethod
    def _assign_if_not_exists(user, badge_name):
        try:
            badge = Badge.objects.get(name=badge_name)
            user_badge, created = UserBadge.objects.get_or_create(user=user, badge=badge)
            if created:
                print(f"🏆 Badge '{badge_name}' assegnato a {user.name}!")
            return created
        except Badge.DoesNotExist:
            print(f"❌ Badge '{badge_name}' non trovato nel database!")
            return False

    @staticmethod
    def check_all_badges_for_user(user):
        """Controlla tutti i badge possibili per un utente - utile per fix/aggiornamenti"""

        # Count posts
        post_count = Post.objects.filter(user=user).count()
        if post_count >= 1:
            BadgeService._assign_if_not_exists(user, 'Primo Post')
        if post_count >= 5:
            BadgeService._assign_if_not_exists(user, 'Fabrizio Corona')

        # Count comments
        comment_count = Comment.objects.filter(user=user).count()
        if comment_count >= 1:
            BadgeService._assign_if_not_exists(user, 'Primo Commento')
        if comment_count >= 10:
            BadgeService._assign_if_not_exists(user, 'Kanye West')

        # Count created groups
        created_groups = TripGroup.objects.filter(creator=user).count()
        if created_groups >= 1:
            BadgeService._assign_if_not_exists(user, 'Fondatore')

        # Count group memberships
        group_memberships = GroupMembership.objects.filter(user=user).count()
        if group_memberships >= 3:
            BadgeService._assign_if_not_exists(user, 'Nico B')

        # Check location posts
        location_posts = Post.objects.filter(user=user, latitude__isnull=False, longitude__isnull=False).count()
        if location_posts >= 1:
            BadgeService._assign_if_not_exists(user, 'Esploratore')

        # Check AI usage
        ai_posts = Post.objects.filter(user=user).exclude(ocr_text='').exclude(object_tags=[]).count()
        if ai_posts >= 1:
            BadgeService._assign_if_not_exists(user, 'm-niky')
        if ai_posts >= 10:
            BadgeService._assign_if_not_exists(user, 'Cucippo')