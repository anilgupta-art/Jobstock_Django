from django.core.management.base import BaseCommand
from zoho_integration.zoho_api_utils import test_upload_dummy_resume

class Command(BaseCommand):
    help = 'Test RPO resume upload with a dummy file.'

    def handle(self, *args, **options):
        result = test_upload_dummy_resume()
        self.stdout.write(self.style.SUCCESS(f'Result: {result}'))
