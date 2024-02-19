from django.core.management.base import BaseCommand
from address.models import AddressType
from django.utils.translation import gettext as _

class Command(BaseCommand):
    help = 'Load address types into the AddressType model'

    def handle(self, *args, **options):
        address_types_data = [
            {"type": AddressType.HOME},
            {"type": AddressType.WORK},
            {"type": AddressType.BILLING},
            {"type": AddressType.DELIVERY},
            {"type": AddressType.MAIN},
        ]

        for data in address_types_data:
            AddressType.objects.get_or_create(type=data["type"])

        self.stdout.write(self.style.SUCCESS('Successfully loaded address types'))