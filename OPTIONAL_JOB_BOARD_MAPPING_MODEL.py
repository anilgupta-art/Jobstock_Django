"""
Optional Model: Job Board Mapping
Add this to models_extended.py if you want to track external job board postings
"""
from django.db import models
from App.models import Job


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
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
    )
    
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='board_mappings'
    )
    board = models.CharField(
        max_length=20,
        choices=BOARD_CHOICES,
        help_text="External job board name"
    )
    external_id = models.CharField(
        max_length=255,
        help_text="Job ID on the external board"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    published_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the job was published to this board"
    )
    last_synced = models.DateTimeField(
        auto_now=True,
        help_text="Last time the job was synced to this board"
    )
    error_message = models.TextField(
        blank=True,
        null=True,
        help_text="Error message if publication failed"
    )
    
    class Meta:
        db_table = 'job_board_mapping'
        unique_together = ('job', 'board')
        verbose_name = 'Job Board Mapping'
        verbose_name_plural = 'Job Board Mappings'
        ordering = ['-published_at']
    
    def __str__(self):
        return f"{self.job.title} on {self.get_board_display()}"


# After adding this model, run:
# python manage.py makemigrations
# python manage.py migrate

# Then update the job_board_integration_service.py methods:

# In _save_board_job_mapping:
# def _save_board_job_mapping(self, job_id: int, board: str, external_id: str) -> None:
#     from App.models_extended import JobBoardMapping
#     JobBoardMapping.objects.update_or_create(
#         job_id=job_id,
#         board=board,
#         defaults={
#             'external_id': external_id,
#             'status': 'active'
#         }
#     )

# In _get_board_mappings:
# def _get_board_mappings(self, job_id: int) -> List[Dict[str, str]]:
#     from App.models_extended import JobBoardMapping
#     return list(JobBoardMapping.objects.filter(
#         job_id=job_id,
#         status='active'
#     ).values('board', 'external_id'))
