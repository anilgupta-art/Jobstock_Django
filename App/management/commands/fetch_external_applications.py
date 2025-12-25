"""
Django Management Command: Fetch applications from external job boards
Usage: python manage.py fetch_external_applications [options]
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from App.models import Job
from App.models.job_board_models import JobBoardMapping
from App.services.job_board_integration_service import job_board_service


class Command(BaseCommand):
    help = 'Fetch applications from external job boards'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--job-id',
            type=int,
            help='Fetch applications for specific job',
        )
        parser.add_argument(
            '--board',
            type=str,
            choices=['indeed', 'ziprecruiter', 'linkedin', 'jobelephant'],
            help='Fetch from specific board only',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Fetch for all active jobs',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Fetching External Applications'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Determine which jobs to fetch for
        if options['job_id']:
            jobs = Job.objects.filter(pk=options['job_id'])
        elif options['all']:
            # Get all jobs with active board mappings
            job_ids = JobBoardMapping.objects.filter(
                status='active'
            ).values_list('job_id', flat=True).distinct()
            jobs = Job.objects.filter(pk__in=job_ids)
        else:
            self.stdout.write(self.style.ERROR(
                "Please specify --job-id or --all"
            ))
            return
        
        board = options.get('board')
        
        self.stdout.write(f"\nFetching applications for {jobs.count()} jobs\n")
        
        total_applications = 0
        
        for job in jobs:
            self.stdout.write(f"Job: {job.title} (ID: {job.id})")
            
            # Fetch applications
            result = job_board_service.fetch_applications(job.id, board)
            
            if result['success']:
                apps_count = result['data'].get('count', 0)
                total_applications += apps_count
                self.stdout.write(self.style.SUCCESS(
                    f"  ✓ Fetched {apps_count} applications"
                ))
                
                # Show breakdown by board
                apps = result['data'].get('applications', [])
                boards_count = {}
                for app in apps:
                    board_name = app.get('source_board', 'unknown')
                    boards_count[board_name] = boards_count.get(board_name, 0) + 1
                
                for board_name, count in boards_count.items():
                    self.stdout.write(f"    - {board_name}: {count}")
            else:
                self.stdout.write(self.style.ERROR(
                    f"  ✗ Error: {result.get('message')}"
                ))
        
        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(
            f"Total Applications Fetched: {total_applications}"
        ))
        self.stdout.write('=' * 60)
