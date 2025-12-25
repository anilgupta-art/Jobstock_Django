from django.core.management.base import BaseCommand
from App.models import NavigationItem

class Command(BaseCommand):
    help = 'Reorder RPO navigation items for Resume Upload page.'

    def handle(self, *args, **options):
        # Define the desired order
        nav_titles = [
            'Posted Jobs',
            'Upload Resumes',
            'All Resumes',
            'Resume Matching',
        ]
        
        updated = 0
        for idx, title in enumerate(nav_titles, start=1):
            qs = NavigationItem.objects.filter(title__iexact=title, is_active=True)
            if not qs.exists():
                self.stdout.write(self.style.WARNING(f'Navigation item not found: {title}'))
                continue
            for item in qs:
                item.order = idx
                item.save(update_fields=['order'])
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Updated order for: {item.title} (id={item.id})'))
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} navigation items.'))
