from django.core.management.base import BaseCommand

from backendtriptales.models import Badge


class Command(BaseCommand):
    def handle(self, *args, **options):
        badges = [
            {"name": "Primo Post", "description": "Hai condiviso il tuo primo ricordo!"},
            {"name": "Fotografo", "description": "Hai condiviso 5 post!"},
            {"name": "Primo Commento", "description": "Hai scritto il tuo primo commento!"},
            {"name": "Chiacchierone", "description": "Hai scritto 10 commenti!"},
            {"name": "Fondatore", "description": "Hai creato il tuo primo gruppo!"},
            {"name": "Membro Attivo", "description": "Fai parte di 3 gruppi!"},
            {"name": "Esploratore", "description": "Hai condiviso la tua prima posizione!"},
            {"name": "Amante dell'IA", "description": "Hai usato l'intelligenza artificiale!"},
        ]

        for badge_data in badges:
            Badge.objects.get_or_create(
                name=badge_data["name"],
                defaults={
                    "description": badge_data["description"],
                    "badge_image_url": "https://example.com/badge.png"
                }
            )

        self.stdout.write("Badge creati con successo!")