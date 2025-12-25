"""
Celery Tasks for Resume-Job Matching
Background processing for AI-powered resume matching
"""
from celery import shared_task
from django.utils import timezone
from App.models import ResumeJobMatch, Job, ResumeProcessing
from App.services.resume_matching_service import ResumeJobMatchingService
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def match_resume_to_job_task(self, job_id, resume_id, user_id=None):
    """
    Background task to match a single resume to a job
    
    Args:
        job_id: Job ID
        resume_id: ResumeProcessing ID
        user_id: User ID who initiated the match
        
    Returns:
        dict: Match result
    """
    try:
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id) if user_id else None
        
        logger.info(f"Starting match: Resume {resume_id} -> Job {job_id}")
        
        result = ResumeJobMatchingService.match_resume_to_job(job_id, resume_id, user)
        
        if result.success:
            logger.info(f"Match completed: {result.data.get('overall_match')}%")
            return {
                'status': 'success',
                'match_id': result.data.get('match_id'),
                'match_percentage': result.data.get('overall_match')
            }
        else:
            logger.error(f"Match failed: {result.message}")
            return {
                'status': 'failed',
                'error': result.message
            }
    
    except Exception as exc:
        logger.error(f"Error in match task: {str(exc)}")
        raise self.retry(exc=exc, countdown=60)


@shared_task(bind=True)
def match_resume_to_all_jobs_task(self, resume_id, user_id=None, filters=None):
    """
    Background task to match a resume to all active jobs
    
    Args:
        resume_id: ResumeProcessing ID
        user_id: User ID who initiated the match
        filters: Optional filters for jobs
        
    Returns:
        dict: Matching results
    """
    try:
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id) if user_id else None
        
        logger.info(f"Starting batch match for Resume {resume_id}")
        
        result = ResumeJobMatchingService.match_resume_to_all_jobs(
            resume_id, user, filters or {}
        )
        
        if result.success:
            total = result.data.get('total_jobs_matched', 0)
            logger.info(f"Batch match completed: {total} jobs")
            return {
                'status': 'success',
                'total_matches': total,
                'resume_id': resume_id
            }
        else:
            logger.error(f"Batch match failed: {result.message}")
            return {
                'status': 'failed',
                'error': result.message
            }
    
    except Exception as exc:
        logger.error(f"Error in batch match task: {str(exc)}")
        return {
            'status': 'error',
            'error': str(exc)
        }


@shared_task(bind=True)
def match_all_resumes_to_job_task(self, job_id, user_id=None, filters=None):
    """
    Background task to match all resumes to a specific job
    
    Args:
        job_id: Job ID
        user_id: User ID who initiated the match
        filters: Optional filters for resumes
        
    Returns:
        dict: Matching results
    """
    try:
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id) if user_id else None
        
        logger.info(f"Starting batch match for Job {job_id}")
        
        # Get all completed resumes
        resumes_query = ResumeProcessing.objects.filter(status='completed')
        
        if filters:
            if filters.get('user_id'):
                resumes_query = resumes_query.filter(user_id=filters['user_id'])
        
        resumes = resumes_query.all()
        
        results = []
        for resume in resumes:
            match_result = ResumeJobMatchingService.match_resume_to_job(
                job_id, resume.id, user
            )
            if match_result.success:
                results.append(match_result.data)
        
        logger.info(f"Batch match completed: {len(results)} resumes matched to Job {job_id}")
        
        return {
            'status': 'success',
            'total_matches': len(results),
            'job_id': job_id
        }
    
    except Exception as exc:
        logger.error(f"Error in batch job match task: {str(exc)}")
        return {
            'status': 'error',
            'error': str(exc)
        }


@shared_task
def cleanup_old_matches_task(days=30):
    """
    Clean up old match records
    
    Args:
        days: Delete matches older than this many days
        
    Returns:
        dict: Cleanup results
    """
    try:
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        deleted_count = ResumeJobMatch.objects.filter(
            created_at__lt=cutoff_date,
            is_recommended=False,
            match_quality='poor'
        ).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old poor-quality matches")
        
        return {
            'status': 'success',
            'deleted_count': deleted_count
        }
    
    except Exception as exc:
        logger.error(f"Error in cleanup task: {str(exc)}")
        return {
            'status': 'error',
            'error': str(exc)
        }


@shared_task
def recalculate_match_task(match_id):
    """
    Recalculate an existing match
    
    Args:
        match_id: ResumeJobMatch ID
        
    Returns:
        dict: Recalculation result
    """
    try:
        match = ResumeJobMatch.objects.select_related('job', 'resume').get(id=match_id)
        
        logger.info(f"Recalculating match {match_id}")
        
        # Recalculate
        match.status = 'processing'
        match.processing_started_at = timezone.now()
        match.save()
        
        match_data = ResumeJobMatchingService.calculate_overall_match(
            match.job, match.resume
        )
        
        if 'error' in match_data:
            match.status = 'failed'
            match.error_message = match_data['error']
            match.save()
            return {
                'status': 'failed',
                'error': match_data['error']
            }
        
        # Update match
        from decimal import Decimal
        match.overall_match_percentage = Decimal(str(match_data['overall_match_percentage']))
        match.skills_match_percentage = Decimal(str(match_data['skills_match_percentage']))
        match.experience_match_percentage = Decimal(str(match_data['experience_match_percentage']))
        match.location_match_percentage = Decimal(str(match_data['location_match_percentage']))
        match.success_reasons = match_data['success_reasons']
        match.failure_reasons = match_data['failure_reasons']
        match.match_quality = match_data['match_quality']
        match.is_recommended = match_data['is_recommended']
        match.detailed_analysis = match_data['detailed_analysis']
        match.status = 'completed'
        match.processing_completed_at = timezone.now()
        match.save()
        
        logger.info(f"Match {match_id} recalculated: {match.overall_match_percentage}%")
        
        return {
            'status': 'success',
            'match_id': match_id,
            'new_percentage': float(match.overall_match_percentage)
        }
    
    except ResumeJobMatch.DoesNotExist:
        return {
            'status': 'error',
            'error': f'Match {match_id} not found'
        }
    except Exception as exc:
        logger.error(f"Error recalculating match {match_id}: {str(exc)}")
        return {
            'status': 'error',
            'error': str(exc)
        }
