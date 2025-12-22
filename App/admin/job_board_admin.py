"""
Django Admin for Job Board Integration
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from App.models.job_board_models import JobBoardMapping, ExternalApplication, BoardSyncLog


@admin.register(JobBoardMapping)
class JobBoardMappingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'job_title_link',
        'board_badge',
        'status_badge',
        'external_job_id',
        'application_count',
        'view_count',
        'published_at',
        'last_synced',
    )
    list_filter = ('board', 'status', 'published_at')
    search_fields = ('job__title', 'external_job_id', 'external_url')
    readonly_fields = (
        'published_at',
        'last_synced',
        'closed_at',
        'last_error_at',
        'response_data_display',
    )
    
    fieldsets = (
        ('Job Information', {
            'fields': ('job', 'board', 'status')
        }),
        ('External Board Details', {
            'fields': ('external_job_id', 'external_url')
        }),
        ('Metrics', {
            'fields': ('view_count', 'application_count')
        }),
        ('Error Tracking', {
            'fields': ('error_count', 'error_message', 'last_error_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('published_at', 'last_synced', 'closed_at'),
            'classes': ('collapse',)
        }),
        ('Response Data', {
            'fields': ('response_data_display',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['sync_to_board', 'close_on_board', 'retry_failed']
    
    def job_title_link(self, obj):
        """Link to job detail"""
        url = reverse('admin:App_job_change', args=[obj.job.id])
        return format_html('<a href="{}">{}</a>', url, obj.job.title)
    job_title_link.short_description = 'Job'
    
    def board_badge(self, obj):
        """Display board with badge"""
        colors = {
            'indeed': '#2164f3',
            'ziprecruiter': '#22c55e',
            'linkedin': '#0077b5',
            'jobelephant': '#f59e0b',
        }
        color = colors.get(obj.board, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_board_display()
        )
    board_badge.short_description = 'Board'
    
    def status_badge(self, obj):
        """Display status with colored badge"""
        colors = {
            'pending': '#f59e0b',
            'active': '#22c55e',
            'paused': '#3b82f6',
            'closed': '#6b7280',
            'error': '#ef4444',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def response_data_display(self, obj):
        """Pretty print response data"""
        if obj.response_data:
            import json
            return format_html(
                '<pre style="background: #f3f4f6; padding: 10px; border-radius: 5px;">{}</pre>',
                json.dumps(obj.response_data, indent=2)
            )
        return '-'
    response_data_display.short_description = 'API Response'
    
    def sync_to_board(self, request, queryset):
        """Sync selected jobs to their boards"""
        from App.services.job_board_integration_service import job_board_service
        
        success_count = 0
        for mapping in queryset:
            result = job_board_service.sync_job_updates(mapping.job.id)
            if result['success']:
                success_count += 1
        
        self.message_user(
            request,
            f"Synced {success_count} out of {queryset.count()} jobs to external boards."
        )
    sync_to_board.short_description = "Sync to external board"
    
    def close_on_board(self, request, queryset):
        """Close selected jobs on their boards"""
        from App.services.job_board_integration_service import job_board_service
        
        for mapping in queryset:
            job_board_service.remove_job_from_boards(mapping.job.id)
            mapping.close()
        
        self.message_user(
            request,
            f"Closed {queryset.count()} jobs on external boards."
        )
    close_on_board.short_description = "Close on external board"
    
    def retry_failed(self, request, queryset):
        """Retry failed postings"""
        failed = queryset.filter(status='error')
        self.sync_to_board(request, failed)
    retry_failed.short_description = "Retry failed postings"


@admin.register(ExternalApplication)
class ExternalApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'candidate_name',
        'candidate_email',
        'job_title_link',
        'source_badge',
        'status_badge',
        'applied_at',
        'received_at',
    )
    list_filter = ('source', 'status', 'applied_at', 'received_at')
    search_fields = (
        'candidate_name',
        'candidate_email',
        'candidate_phone',
        'job__title',
        'external_application_id'
    )
    readonly_fields = (
        'external_application_id',
        'applied_at',
        'received_at',
        'reviewed_at',
        'application_data_display',
    )
    
    fieldsets = (
        ('Candidate Information', {
            'fields': ('candidate_name', 'candidate_email', 'candidate_phone')
        }),
        ('Job & Source', {
            'fields': ('job', 'source', 'board_mapping', 'external_application_id')
        }),
        ('Application Materials', {
            'fields': ('resume_url', 'resume_file', 'cover_letter')
        }),
        ('Status', {
            'fields': ('status', 'internal_notes')
        }),
        ('Timestamps', {
            'fields': ('applied_at', 'received_at', 'reviewed_at'),
            'classes': ('collapse',)
        }),
        ('Application Data', {
            'fields': ('application_data_display',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_reviewed', 'shortlist_candidates', 'reject_candidates']
    
    def job_title_link(self, obj):
        """Link to job"""
        url = reverse('admin:App_job_change', args=[obj.job.id])
        return format_html('<a href="{}">{}</a>', url, obj.job.title)
    job_title_link.short_description = 'Job'
    
    def source_badge(self, obj):
        """Display source with badge"""
        colors = {
            'indeed': '#2164f3',
            'ziprecruiter': '#22c55e',
            'linkedin': '#0077b5',
            'jobelephant': '#f59e0b',
            'direct': '#6b7280',
        }
        color = colors.get(obj.source, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_source_display()
        )
    source_badge.short_description = 'Source'
    
    def status_badge(self, obj):
        """Display status with badge"""
        colors = {
            'new': '#3b82f6',
            'reviewed': '#8b5cf6',
            'shortlisted': '#22c55e',
            'rejected': '#ef4444',
            'hired': '#10b981',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def application_data_display(self, obj):
        """Pretty print application data"""
        if obj.application_data:
            import json
            return format_html(
                '<pre style="background: #f3f4f6; padding: 10px; border-radius: 5px; max-height: 400px; overflow: auto;">{}</pre>',
                json.dumps(obj.application_data, indent=2)
            )
        return '-'
    application_data_display.short_description = 'Full Application Data'
    
    def mark_reviewed(self, request, queryset):
        """Mark as reviewed"""
        count = 0
        for app in queryset.filter(status='new'):
            app.mark_as_reviewed()
            count += 1
        self.message_user(request, f"Marked {count} applications as reviewed.")
    mark_reviewed.short_description = "Mark as reviewed"
    
    def shortlist_candidates(self, request, queryset):
        """Shortlist candidates"""
        count = 0
        for app in queryset.exclude(status__in=['rejected', 'hired']):
            app.shortlist()
            count += 1
        self.message_user(request, f"Shortlisted {count} candidates.")
    shortlist_candidates.short_description = "Shortlist"
    
    def reject_candidates(self, request, queryset):
        """Reject candidates"""
        count = 0
        for app in queryset.exclude(status__in=['rejected', 'hired']):
            app.reject()
            count += 1
        self.message_user(request, f"Rejected {count} candidates.")
    reject_candidates.short_description = "Reject"


@admin.register(BoardSyncLog)
class BoardSyncLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'action_badge',
        'board',
        'status_badge',
        'job_link',
        'duration_seconds',
        'started_at',
    )
    list_filter = ('action', 'status', 'board', 'started_at')
    search_fields = ('job__title', 'board', 'error_message')
    readonly_fields = (
        'started_at',
        'completed_at',
        'duration_seconds',
        'request_data_display',
        'response_data_display',
    )
    
    fieldsets = (
        ('Action Details', {
            'fields': ('action', 'board', 'status', 'job', 'board_mapping')
        }),
        ('Request Data', {
            'fields': ('request_data_display',),
            'classes': ('collapse',)
        }),
        ('Response Data', {
            'fields': ('response_data_display', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration_seconds')
        }),
    )
    
    def action_badge(self, obj):
        """Display action with badge"""
        return format_html(
            '<span style="background-color: #6366f1; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            obj.get_action_display()
        )
    action_badge.short_description = 'Action'
    
    def status_badge(self, obj):
        """Display status with badge"""
        colors = {
            'success': '#22c55e',
            'error': '#ef4444',
            'partial': '#f59e0b',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def job_link(self, obj):
        """Link to job if available"""
        if obj.job:
            url = reverse('admin:App_job_change', args=[obj.job.id])
            return format_html('<a href="{}">{}</a>', url, obj.job.title)
        return '-'
    job_link.short_description = 'Job'
    
    def request_data_display(self, obj):
        """Pretty print request data"""
        if obj.request_data:
            import json
            return format_html(
                '<pre style="background: #f3f4f6; padding: 10px; border-radius: 5px; max-height: 400px; overflow: auto;">{}</pre>',
                json.dumps(obj.request_data, indent=2)
            )
        return '-'
    request_data_display.short_description = 'Request Data'
    
    def response_data_display(self, obj):
        """Pretty print response data"""
        if obj.response_data:
            import json
            return format_html(
                '<pre style="background: #f3f4f6; padding: 10px; border-radius: 5px; max-height: 400px; overflow: auto;">{}</pre>',
                json.dumps(obj.response_data, indent=2)
            )
        return '-'
    response_data_display.short_description = 'Response Data'
