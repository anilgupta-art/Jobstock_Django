"""
Django Signals for Job Board Integration
Auto-publish jobs to boards when created/updated
"""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from App.models import Job
from App.models.job_board_models import JobBoardMapping
from App.services.job_board_integration_service import job_board_service
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Job)
def auto_publish_job_to_boards(sender, instance, created, **kwargs):
    """
    Automatically publish job to configured boards when created
    """
    # Only auto-publish if enabled in settings
    if not getattr(settings, 'AUTO_PUBLISH_JOBS_TO_BOARDS', False):
        return
    
    # Only for new jobs
    if not created:
        return
    
    # Only if job is active
    if not instance.is_active:
        return
    
    # Get default boards from settings
    default_boards = getattr(settings, 'DEFAULT_JOB_BOARDS', [])
    
    if not default_boards:
        return
    
    logger.info(f"Auto-publishing job {instance.id} to boards: {default_boards}")
    
    # Publish to boards
    try:
        result = job_board_service.publish_to_multiple_boards(
            instance.id,
            default_boards
        )
        
        if result['success']:
            logger.info(f"Successfully published job {instance.id} to {result['data']['successful']} boards")
        else:
            logger.error(f"Failed to auto-publish job {instance.id}: {result.get('message')}")
    
    except Exception as e:
        logger.error(f"Error auto-publishing job {instance.id}: {e}", exc_info=True)


@receiver(post_save, sender=Job)
def sync_job_updates_to_boards(sender, instance, created, **kwargs):
    """
    Sync job updates to external boards when job is modified
    """
    # Skip for new jobs (handled by auto_publish)
    if created:
        return
    
    # Only sync if enabled in settings
    if not getattr(settings, 'AUTO_SYNC_JOB_UPDATES', False):
        return
    
    # Check if job has active board mappings
    active_mappings = JobBoardMapping.objects.filter(
        job=instance,
        status='active'
    )
    
    if not active_mappings.exists():
        return
    
    logger.info(f"Auto-syncing updates for job {instance.id} to external boards")
    
    try:
        result = job_board_service.sync_job_updates(instance.id)
        
        if result['success']:
            logger.info(f"Successfully synced job {instance.id} updates")
        else:
            logger.error(f"Failed to sync job {instance.id} updates: {result.get('message')}")
    
    except Exception as e:
        logger.error(f"Error syncing job {instance.id} updates: {e}", exc_info=True)


@receiver(pre_delete, sender=Job)
def remove_job_from_boards(sender, instance, **kwargs):
    """
    Remove job from external boards when deleted
    """
    # Only if enabled in settings
    if not getattr(settings, 'AUTO_REMOVE_JOBS_FROM_BOARDS', True):
        return
    
    # Check if job has active board mappings
    active_mappings = JobBoardMapping.objects.filter(
        job=instance,
        status='active'
    )
    
    if not active_mappings.exists():
        return
    
    logger.info(f"Removing job {instance.id} from external boards before deletion")
    
    try:
        result = job_board_service.remove_job_from_boards(instance.id)
        
        if result['success']:
            logger.info(f"Successfully removed job {instance.id} from boards")
        else:
            logger.error(f"Failed to remove job {instance.id} from boards: {result.get('message')}")
    
    except Exception as e:
        logger.error(f"Error removing job {instance.id} from boards: {e}", exc_info=True)
