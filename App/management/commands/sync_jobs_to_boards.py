"""
Django Management Command: Sync jobs to external job boards
Usage: python manage.py sync_jobs_to_boards [options]
"""
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from App.models import Job
from App.models.job_board_models import JobBoardMapping
from App.services.job_board_integration_service import job_board_service


class Command(BaseCommand):
    help = 'Sync jobs to external job boards'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--job-id',
            type=int,
            help='Sync specific job by ID',
        )
        parser.add_argument(
            '--board',
            type=str,
            choices=['indeed', 'ziprecruiter', 'linkedin', 'jobelephant'],
            help='Sync to specific board',
        )
        parser.add_argument(
            '--active-only',
            action='store_true',
            help='Only sync active jobs',
        )
        parser.add_argument(
            '--retry-failed',
            action='store_true',
            help='Retry failed postings',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be synced without actually syncing',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Job Board Sync'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Build query
        if options['job_id']:
            jobs = Job.objects.filter(pk=options['job_id'])
            if not jobs.exists():
                raise CommandError(f"Job with ID {options['job_id']} does not exist")
        elif options['active_only']:
            jobs = Job.objects.filter(is_active=True)
        else:
            jobs = Job.objects.all()
        
        # Filter by board if specified
        board = options.get('board')
        
        # Retry failed postings
        if options['retry_failed']:
            self.retry_failed_postings(board, options['dry_run'])
            return
        
        # Sync jobs
        success_count = 0
        error_count = 0
        
        self.stdout.write(f"\nFound {jobs.count()} jobs to sync")
        
        for job in jobs:
            self.stdout.write(f"\n{'[DRY RUN] ' if options['dry_run'] else ''}Syncing: {job.title} (ID: {job.id})")
            
            if options['dry_run']:
                # Show what would be synced
                mappings = JobBoardMapping.objects.filter(job=job, status='active')
                if board:
                    mappings = mappings.filter(board=board)
                
                for mapping in mappings:
                    self.stdout.write(f"  → Would sync to {mapping.get_board_display()}")
                continue
            
            # Actual sync
            result = job_board_service.sync_job_updates(job.id)
            
            if result['success']:
                self.stdout.write(self.style.SUCCESS(f"  ✓ Synced successfully"))
                success_count += 1
            else:
                self.stdout.write(self.style.ERROR(f"  ✗ Sync failed: {result.get('message')}"))
                error_count += 1
        
        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f"Sync Complete!"))
        self.stdout.write(f"  Success: {success_count}")
        self.stdout.write(f"  Errors: {error_count}")
        self.stdout.write('=' * 60)
    
    def retry_failed_postings(self, board, dry_run):
        """Retry failed postings"""
        self.stdout.write("\nRetrying failed postings...")
        
        # Get failed mappings
        failed = JobBoardMapping.objects.filter(status='error')
        if board:
            failed = failed.filter(board=board)
        
        self.stdout.write(f"Found {failed.count()} failed postings")
        
        success_count = 0
        
        for mapping in failed:
            self.stdout.write(f"\nRetrying: {mapping.job.title} on {mapping.get_board_display()}")
            
            if dry_run:
                self.stdout.write("  → Would retry posting")
                continue
            
            # Retry posting
            result = job_board_service.publish_job(mapping.job.id, mapping.board)
            
            if result['success']:
                mapping.mark_as_active()
                self.stdout.write(self.style.SUCCESS("  ✓ Retry successful"))
                success_count += 1
            else:
                self.stdout.write(self.style.ERROR(f"  ✗ Retry failed: {result.get('message')}"))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(f"Retry Complete: {success_count} succeeded")
        self.stdout.write('=' * 60)
