from django.core.management.base import BaseCommand
from App.models import NavigationItem

class Command(BaseCommand):
    help = 'List all navigation items for RPO navigation.'

    def handle(self, *args, **options):
        items = NavigationItem.objects.filter(is_active=True).order_by('order')
        for item in items:
            self.stdout.write(f"ID={item.id} | Title='{item.title}' | Order={item.order} | URL={item.url_name}")
