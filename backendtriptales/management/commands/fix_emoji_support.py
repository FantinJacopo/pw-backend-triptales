from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix database charset for emoji support'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                # Aggiorna il charset del database
                self.stdout.write('Aggiornamento charset database...')
                cursor.execute("ALTER DATABASE pwtriptales_db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;")

                # Aggiorna il charset della tabella comments
                self.stdout.write('Aggiornamento tabella comments...')
                cursor.execute(
                    "ALTER TABLE backendtriptales_comment CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

                # Aggiorna specificamente il campo content
                self.stdout.write('Aggiornamento campo content...')
                cursor.execute(
                    "ALTER TABLE backendtriptales_comment MODIFY content TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

                # Aggiorna anche altri campi di testo che potrebbero contenere emoji
                self.stdout.write('Aggiornamento altri campi di testo...')
                cursor.execute(
                    "ALTER TABLE backendtriptales_post MODIFY smart_caption VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                cursor.execute(
                    "ALTER TABLE backendtriptales_post MODIFY ocr_text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                cursor.execute(
                    "ALTER TABLE backendtriptales_tripgroup MODIFY group_name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                cursor.execute(
                    "ALTER TABLE backendtriptales_tripgroup MODIFY description TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                cursor.execute(
                    "ALTER TABLE backendtriptales_user MODIFY name VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")

                self.stdout.write(self.style.SUCCESS('✅ Database aggiornato con successo per il supporto emoji!'))

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Errore durante l\'aggiornamento: {str(e)}')
                )
                self.stdout.write('Verifica che XAMPP sia avviato e che tu abbia i permessi necessari.')