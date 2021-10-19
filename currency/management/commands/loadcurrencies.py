from django.core.management.base import BaseCommand  # , CommandError

from currency.services import load_currencies_data  # , ServiceError


class Command(BaseCommand):

    def handle(self, *args, **options):
        load_currencies_data()
        self.stdout.write(self.style.SUCCESS('Successfully load currencies'))
