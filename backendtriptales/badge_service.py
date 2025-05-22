from .models import Badge, UserBadge, User


class BadgeService:
    @staticmethod
    def check_and_assign_badges(user, action_type, **kwargs):
        """Controlla e assegna badge basati sull'azione"""

        if action_type == 'first_post':
            BadgeService._assign_if_not_exists(user, 'Primo Post')

        elif action_type == 'post_count':
            post_count = kwargs.get('count', 0)
            if post_count >= 5:
                BadgeService._assign_if_not_exists(user, 'Fotografo')

        elif action_type == 'first_comment':
            BadgeService._assign_if_not_exists(user, 'Primo Commento')

        elif action_type == 'comment_count':
            comment_count = kwargs.get('count', 0)
            if comment_count >= 10:
                BadgeService._assign_if_not_exists(user, 'Chiacchierone')

        elif action_type == 'first_group':
            BadgeService._assign_if_not_exists(user, 'Fondatore')

        elif action_type == 'group_membership':
            group_count = kwargs.get('count', 0)
            if group_count >= 3:
                BadgeService._assign_if_not_exists(user, 'Membro Attivo')

        elif action_type == 'first_location':
            BadgeService._assign_if_not_exists(user, 'Esploratore')

        elif action_type == 'first_ai':
            BadgeService._assign_if_not_exists(user, 'Amante dell\'IA')

    @staticmethod
    def _assign_if_not_exists(user, badge_name):
        try:
            badge = Badge.objects.get(name=badge_name)
            UserBadge.objects.get_or_create(user=user, badge=badge)
        except Badge.DoesNotExist:
            pass