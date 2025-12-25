"""
Job Board Integration Models
Tracks external job board postings and applications
"""
from django.db import models
from django.utils import timezone


class JobBoardMapping(models.Model):
    """
    Tracks jobs posted to external job boards
    Maps internal job IDs to external board IDs
    """
    
    BOARD_CHOICES = (
        ('indeed', 'Indeed'),
        ('ziprecruiter', 'ZipRecruiter'),
        ('linkedin', 'LinkedIn'),
        ('jobelephant', 'JobElephant'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
        ('error', 'Error'),
    )
    
    # Relationships
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name='board_mappings',
        help_text="Internal job posting"
    )
    
    # Board Information
    board = models.CharField(
        max_length=20,
        choices=BOARD_CHOICES,
        help_text="External job board name"
    )
    external_job_id = models.CharField(
        max_length=255,
        help_text="Job ID on the external board"
    )
    external_url = models.URLField(
        blank=True,
        null=True,
        help_text="Direct URL to job on external board"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Timestamps
    published_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the job was published to this board"
    )
    last_synced = models.DateTimeField(
        auto_now=True,
        help_text="Last time the job was synced to this board"
    )
    closed_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the job was closed on this board"
    )
    
    # Error Tracking
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Error message if publication failed"
    )
    error_count = models.IntegerField(
        default=0,
        help_text="Number of errors encountered"
    )
    last_error_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When the last error occurred"
    )
    
    # Metrics
    view_count = models.IntegerField(
        default=0,
        help_text="Number of views on external board"
    )
    application_count = models.IntegerField(
        default=0,
        help_text="Number of applications from this board"
    )
    
    # Metadata
    response_data = models.JSONField(
        blank=True,
        null=True,
        help_text="Full API response from board"
    )
    
    class Meta:
        db_table = 'job_board_mapping'
        unique_together = [['job', 'board']]
        verbose_name = 'Job Board Mapping'
        verbose_name_plural = 'Job Board Mappings'
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['board', 'status']),
            models.Index(fields=['job', 'status']),
            models.Index(fields=['external_job_id']),
        ]
    
    def __str__(self):
        return f"{self.job.title} on {self.get_board_display()} ({self.status})"
    
    def mark_as_active(self):
        """Mark the mapping as active"""
        self.status = 'active'
        self.error_count = 0
        self.error_message = None
        self.save(update_fields=['status', 'error_count', 'error_message', 'last_synced'])
    
    def mark_as_error(self, error_message: str):
        """Mark the mapping as having an error"""
        self.status = 'error'
        self.error_message = error_message
        self.error_count += 1
        self.last_error_at = timezone.now()
        self.save(update_fields=['status', 'error_message', 'error_count', 'last_error_at', 'last_synced'])
    
    def close(self):
        """Mark the job as closed on this board"""
        self.status = 'closed'
        self.closed_at = timezone.now()
        self.save(update_fields=['status', 'closed_at', 'last_synced'])
    
    def increment_views(self, count: int = 1):
        """Increment view count"""
        self.view_count += count
        self.save(update_fields=['view_count', 'last_synced'])
    
    def increment_applications(self, count: int = 1):
        """Increment application count"""
        self.application_count += count
        self.save(update_fields=['application_count', 'last_synced'])
    
    def is_active(self) -> bool:
        """Check if mapping is active"""
        return self.status == 'active'
    
    def get_status_badge_class(self) -> str:
        """Get Bootstrap badge class for status"""
        status_classes = {
            'pending': 'badge-warning',
            'active': 'badge-success',
            'paused': 'badge-info',
            'closed': 'badge-secondary',
            'error': 'badge-danger',
        }
        return status_classes.get(self.status, 'badge-secondary')


class ExternalApplication(models.Model):
    """
    Stores applications received from external job boards
    """
    
    SOURCE_CHOICES = (
        ('indeed', 'Indeed'),
        ('ziprecruiter', 'ZipRecruiter'),
        ('linkedin', 'LinkedIn'),
        ('jobelephant', 'JobElephant'),
        ('direct', 'Direct Application'),
    )
    
    STATUS_CHOICES = (
        ('new', 'New'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )
    
    # Relationships
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name='external_applications',
        help_text="Job being applied to"
    )
    board_mapping = models.ForeignKey(
        JobBoardMapping,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
        help_text="Source board mapping"
    )
    
    # External IDs
    external_application_id = models.CharField(
        max_length=255,
        unique=True,
        help_text="Application ID from external board"
    )
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='direct'
    )
    
    # Candidate Information
    candidate_name = models.CharField(max_length=255)
    candidate_email = models.EmailField()
    candidate_phone = models.CharField(max_length=30, blank=True)
    
    # Resume
    resume_url = models.URLField(
        blank=True,
        null=True,
        help_text="URL to resume on external board"
    )
    resume_file = models.FileField(
        upload_to='external_resumes/',
        blank=True,
        null=True,
        help_text="Downloaded resume file"
    )
    
    # Application Data
    cover_letter = models.TextField(blank=True)
    application_data = models.JSONField(
        blank=True,
        null=True,
        help_text="Full application data from board"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    
    # Timestamps
    applied_at = models.DateTimeField(
        help_text="When candidate applied on external board"
    )
    received_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When we received this application"
    )
    reviewed_at = models.DateTimeField(
        blank=True,
        null=True
    )
    
    # Notes
    internal_notes = models.TextField(
        blank=True,
        help_text="Internal notes about this application"
    )
    
    class Meta:
        db_table = 'external_application'
        verbose_name = 'External Application'
        verbose_name_plural = 'External Applications'
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['job', 'status']),
            models.Index(fields=['source', 'status']),
            models.Index(fields=['candidate_email']),
        ]
    
    def __str__(self):
        return f"{self.candidate_name} - {self.job.title} (via {self.get_source_display()})"
    
    def mark_as_reviewed(self):
        """Mark application as reviewed"""
        self.status = 'reviewed'
        self.reviewed_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_at'])
    
    def shortlist(self):
        """Shortlist this candidate"""
        self.status = 'shortlisted'
        self.save(update_fields=['status'])
    
    def reject(self, reason: str = ""):
        """Reject this application"""
        self.status = 'rejected'
        if reason:
            self.internal_notes = f"{self.internal_notes}\n\nRejection reason: {reason}".strip()
        self.save(update_fields=['status', 'internal_notes'])


class BoardSyncLog(models.Model):
    """
    Logs synchronization activities with external boards
    """
    
    ACTION_CHOICES = (
        ('post', 'Post Job'),
        ('update', 'Update Job'),
        ('close', 'Close Job'),
        ('fetch_apps', 'Fetch Applications'),
        ('sync', 'Sync Status'),
    )
    
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('error', 'Error'),
        ('partial', 'Partial Success'),
    )
    
    # Relationships
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name='sync_logs',
        null=True,
        blank=True
    )
    board_mapping = models.ForeignKey(
        JobBoardMapping,
        on_delete=models.CASCADE,
        related_name='sync_logs',
        null=True,
        blank=True
    )
    
    # Action Details
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )
    board = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    
    # Request/Response
    request_data = models.JSONField(
        blank=True,
        null=True,
        help_text="Data sent to external board"
    )
    response_data = models.JSONField(
        blank=True,
        null=True,
        help_text="Response from external board"
    )
    error_message = models.TextField(blank=True)
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        blank=True,
        null=True
    )
    duration_seconds = models.FloatField(
        blank=True,
        null=True,
        help_text="Duration in seconds"
    )
    
    class Meta:
        db_table = 'board_sync_log'
        verbose_name = 'Board Sync Log'
        verbose_name_plural = 'Board Sync Logs'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['board', 'status']),
            models.Index(fields=['action', 'status']),
            models.Index(fields=['-started_at']),
        ]
    
    def __str__(self):
        return f"{self.get_action_display()} on {self.board} - {self.get_status_display()}"
    
    def complete(self, success: bool = True, response_data: dict = None, error: str = None):
        """Mark sync as completed"""
        from datetime import datetime
        
        self.completed_at = timezone.now()
        self.duration_seconds = (self.completed_at - self.started_at).total_seconds()
        self.status = 'success' if success else 'error'
        
        if response_data:
            self.response_data = response_data
        if error:
            self.error_message = error
        
        self.save()
