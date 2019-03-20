from django.core.management.base import BaseCommand
from django.db.models import Min
from municipalities.models import Municipality


class Command(BaseCommand):
    help = 'Sets the minimal zip_code of a bfs_number group as the ' \
           'main-municipality'

    def handle(self, *args, **options):
        municipalities = \
            Municipality.objects.values('bfs_number')\
                                .annotate(Min('zip_code'))\
                                .annotate(Min('id'))

        for m in municipalities:
            main_municipality = Municipality.objects.get(id=m['id__min'])
            print(
                main_municipality.bfs_number,
                main_municipality.zip_code,
                main_municipality.name)
            main_municipality.main_municipality = True
            main_municipality.save()
