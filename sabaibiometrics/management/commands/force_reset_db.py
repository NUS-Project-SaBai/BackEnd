from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Forcefully resets the database by terminating active connections and resetting the database'

    def handle(self, *args, **kwargs):
        confirm = input("You have requested a database reset.\n This will IRREVERSIBLY DESTROY ALL data in the database 'postgres'.\n Are you sure you want to do this?\n Type 'yes' to continue, or 'no' to cancel: ")
        if confirm != 'yes':
            self.stdout.write(self.style.ERROR('Database reset cancelled.'))
            return
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = current_database()
                  AND pid <> pg_backend_pid();
            """)
        self.stdout.write(self.style.SUCCESS(
            'Terminated all active connections.'))
        call_command('reset_db', interactive=False)
        self.stdout.write(self.style.SUCCESS('Database reset successfully!'))
