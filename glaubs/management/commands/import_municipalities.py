from django.core.management.base import BaseCommand
from municipalities.models import Municipality
import csv


class Command(BaseCommand):
    help = 'Imports municipalities'

    def add_arguments(self, parser):
        parser.add_argument('municipality_file', type=str)

    def handle(self, *args, **options):
        with open(options['municipality_file'], 'r') as f:
            csvf = csv.reader(f)

            for idx, row in enumerate(csvf):
                if idx == 0:
                    continue

                canton = row[0]
                name = row[2]
                bfs_number = row[4]
                zip_code = row[7]
                Municipality.objects.create(
                    canton=canton,
                    name=name,
                    bfs_number=bfs_number,
                    zip_code=zip_code)
