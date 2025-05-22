from django.core.management.base import BaseCommand
from backendtriptales.models import Badge


class Command(BaseCommand):
    help = 'Popola il database con i badge predefiniti'

    def handle(self, *args, **options):
        badges = [
            {
                'name': 'Primo Post',
                'description': 'Hai pubblicato il tuo primo post! Benvenuto nella community di TripTales!',
                'badge_image_url': 'https://example.com/badges/first_post.png'
            },
            {
                'name': 'Fabrizio Corona',
                'description': 'Sei un vero paparazzo! Hai condiviso 10 foto con i tuoi compagni di viaggio.',
                'badge_image_url': 'https://example.com/badges/photographer.png'
            },
            {
                'name': 'Primo Commento',
                'description': 'Hai lasciato il tuo primo commento! Grazie per aver partecipato alla conversazione.',
                'badge_image_url': 'https://example.com/badges/first_comment.png'
            },
            {
                'name': 'Kanye West',
                'description': 'Sei un vero chiacchierone! Hai scritto 20 commenti.',
                'badge_image_url': 'https://example.com/badges/talkative.png'
            },
            {
                'name': 'Fondatore',
                'description': 'Hai creato il tuo primo gruppo! Sei un vero leader e organizzatore di avventure.',
                'badge_image_url': 'https://example.com/badges/founder.png'
            },
            {
                'name': 'Nico B',
                'description': 'Badge speciale per utenti eccezionali che contribuiscono attivamente alla community.',
                'badge_image_url': 'https://example.com/badges/star.png'
            },
            {
                'name': 'PLC',
                'description': 'Esploratore certificato! Hai condiviso 5 post con geolocalizzazione.',
                'badge_image_url': 'https://example.com/badges/explorer.png'
            },
            {
                'name': 'm-niky',
                'description': 'Maestro dell\'intelligenza artificiale! Hai utilizzato tutte le funzionalità AI dell\'app.',
                'badge_image_url': 'https://example.com/badges/ai_master.png'
            },
            {
                'name': 'Cucippo',
                'description': 'Badge leggendario per i membri più cool della community!',
                'badge_image_url': 'https://example.com/badges/cool.png'
            },
        ]

        created_count = 0
        updated_count = 0

        for badge_data in badges:
            badge, created = Badge.objects.update_or_create(
                name=badge_data['name'],
                defaults={
                    'description': badge_data['description'],
                    'badge_image_url': badge_data['badge_image_url']
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Creato badge: {badge.name}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'🔄 Aggiornato badge: {badge.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✨ Operazione completata! '
                f'Creati: {created_count}, Aggiornati: {updated_count}'
            )
        )