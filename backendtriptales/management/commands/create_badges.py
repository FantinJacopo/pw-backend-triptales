from django.core.management.base import BaseCommand

from backendtriptales.models import Badge


class Command(BaseCommand):
    help = 'Crea i badge di base per l\'applicazione'

    def handle(self, *args, **options):
        badges = [
            {"name": "Primo Post", "description": "Hai condiviso il tuo primo ricordo!"},
            {"name": "Fabrizio Corona", "description": "Hai condiviso 5 post!"},
            {"name": "Primo Commento", "description": "Hai scritto il tuo primo commento!"},
            {"name": "Kanye West", "description": "Hai scritto 10 commenti, non ti bastava X?"},
            {"name": "Fondatore", "description": "Hai creato il tuo primo gruppo!"},
            {"name": "Nico B", "description": "Fai parte di 3 gruppi, sei il Main Character!"},
            {"name": "Esploratore", "description": "Hai condiviso la tua prima posizione!"},
            {"name": "m-niky", "description": "Hai usato l'intelligenza artificiale!"},
            {"name": "Cucippo", "description": "Hai usato l'IA 10 volte! Ami proprio l'intelligenza artificiale!"},
        ]

        created_count = 0
        for badge_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=badge_data["name"],
                defaults={
                    "description": badge_data["description"],
                    "badge_image_url": "https://via.placeholder.com/64x64/4CAF50/FFFFFF?text=🏆"
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Badge creato: {badge.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Badge già esistente: {badge.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Processo completato! {created_count} nuovi badge creati.')
        )