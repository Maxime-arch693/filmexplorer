import csv
from django.core.management.base import BaseCommand
from films.models import Film2

class Command(BaseCommand):
    help = 'Populates the Film model with initial data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                # Utilisation du lecteur CSV classique (séparé par des virgules)
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        film, created = Film2.objects.get_or_create(
                            title=row['English Title'],       # En-tête exact de ton CSV
                            release_year=int(row['Release Year']) # En-tête exact de ton CSV
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"Created film: {film.title}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Film already exists: {film.title}"))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Could not create film {row['English Title']}: {e}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
