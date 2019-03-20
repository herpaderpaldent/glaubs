from django.core.management.base import BaseCommand
from municipalities.models import Municipality
import csv


class Command(BaseCommand):
    help = 'Imports addresses and matches them to municipalities'

    def add_arguments(self, parser):
        parser.add_argument('address_file', type=str)

    def handle(self, *args, **options):
        with open(options['address_file'], 'r') as f:
            csvf = csv.reader(f, delimiter='\t')

            for idx, row in enumerate(csvf):
                if idx == 0:
                    continue

                zip_code = row[3]
                if not zip_code:
                    zip_code = row[0]
                address = '\n'.join([row[1], row[2], zip_code + ' ' + row[4]])
                place = row[4]

                found = False
                municipalities = \
                    Municipality.objects.filter(zip_code=zip_code, name=place)
                for m in municipalities:
                    found = True
                    self._update_municipality(address, m, row)

                if not found:
                    print(u'Not found {} {}'.format(zip_code, place))
                    municipalities = \
                        Municipality.objects.filter(zip_code=zip_code)
                    for m in municipalities:
                        print(u'* Updating {} {}'.format(m.zip_code, m.name))
                        self._update_municipality(address, m, row)

    def _update_municipality(self, address, m, row):
        m.address = address
        m.phone_number = row[5]
        m.email = row[7]
        m.website = row[8]
        m.main_municipality = True
        m.save()
