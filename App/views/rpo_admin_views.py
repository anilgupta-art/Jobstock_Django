"""
RPO Admin Dashboard Views
Following MVT pattern with service layer integration
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator

from App.services.resume_upload_service import ResumeUploadService
from App.services.job_service import JobService
from App.utils.response import ApiResponse
from App.models import Job


@login_required
@require_http_methods(["GET", "POST"])
def rpo_resume_upload(request):
    """
    RPO Admin Resume Upload Page
    GET: Display upload form with statistics, job title, and ResumeSource dropdown
    POST: Handle multiple resume uploads
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()

    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')

    # Get jobid from query params (for GET and POST)
    job_id = request.GET.get('jobid') or request.POST.get('jobid')
    job_title = None
    job_company = None
    if job_id:
        try:
            job_obj = Job.objects.get(pk=job_id)
            job_title = job_obj.title
            job_company = getattr(job_obj, 'company_name', None)
        except Job.DoesNotExist:
            job_title = None
            job_company = None

    # Get ResumeSource companies for dropdown
    from App.models import DropdownGroup, DropdownMaster
    try:
        resume_source_group = DropdownGroup.objects.get(text='ResumeSource', is_active=True)
        resume_sources = DropdownMaster.objects.filter(group=resume_source_group, is_active=True).order_by('sort_order', 'text')
    except DropdownGroup.DoesNotExist:
        resume_sources = []

    if request.method == 'POST':
        # Handle file upload
        files = request.FILES.getlist('resumes')
        resumesource_id = request.POST.get('resume_sources')
        job_obj = None
        resumesource_obj = None
        if job_id:
            try:
                job_obj = Job.objects.get(pk=job_id)
            except Job.DoesNotExist:
                job_obj = None
        if resumesource_id:
            from App.models import DropdownMaster
            try:
                resumesource_obj = DropdownMaster.objects.get(pk=resumesource_id)
            except DropdownMaster.DoesNotExist:
                resumesource_obj = None
        if not files:
            messages.error(request, 'Please select at least one resume file to upload')
            return redirect('App:rpo_resume_upload')
        # Use service to upload resumes
        result = ResumeUploadService.upload_resumes(files, request.user, job=job_obj, resumesource=resumesource_obj)
        if result.success:
            messages.success(request, result.message)
            if result.data['failed_count'] > 0:
                for failed in result.data['failed']:
                    messages.warning(request, f"{failed['filename']}: {failed['error']}")
        else:
            messages.error(request, result.message)
            if hasattr(result, 'error_details') and result.error_details:
                for failed in result.error_details.get('failed', []):
                    messages.error(request, f"{failed['filename']}: {failed['error']}")
        return redirect('App:rpo_resume_upload')

    # GET request - show upload form
    stats_response = ResumeUploadService.get_upload_statistics(request.user)
    stats = stats_response.data if stats_response.success else {}
    resumes_response = ResumeUploadService.get_user_resumes(request.user, limit=10)
    resumes = resumes_response.data.get('resumes', []) if resumes_response.success else []

    job_display = job_title if job_title else ''
    if job_title and job_company:
        job_display = f"{job_title} ({job_company})"
    context = {
        'page_title': 'Resume Upload',
        'stats': stats,
        'recent_uploads': resumes,
        'allowed_extensions': ', '.join(ResumeUploadService.ALLOWED_EXTENSIONS),
        'max_file_size_mb': ResumeUploadService.MAX_FILE_SIZE / (1024 * 1024),
        'job_id': job_id,
        'job_title': job_display,
        'resume_sources': resume_sources,
    }
    return render(request, 'Pages/RPO-Admin/resume_upload.html', context)


@login_required
def rpo_dashboard(request):
    """
    RPO Admin Dashboard
    Main dashboard page for RPO administrators
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get dashboard statistics
    stats_response = ResumeUploadService.get_upload_statistics(request.user)
    stats = stats_response.data if stats_response.success else {}
    
    # Get recent uploads
    resumes_response = ResumeUploadService.get_user_resumes(request.user, limit=5)
    recent_resumes = resumes_response.data.get('resumes', []) if resumes_response.success else []
    
    context = {
        'page_title': 'RPO Admin Dashboard',
        'stats': stats,
        'recent_resumes': recent_resumes
    }
    
    return render(request, 'Pages/RPO-Admin/dashboard.html', context)


@login_required
def rpo_resume_list(request):
    """
    RPO Admin Resume List
    View all uploaded resumes with pagination
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get pagination parameters
    limit = int(request.GET.get('limit', 20))
    offset = int(request.GET.get('offset', 0))

    # Filtering
    job_filter = request.GET.getlist('job')
    resumesource_filter = request.GET.getlist('resumesource')
    status_filter = request.GET.getlist('status')

    from App.models import ResumeProcessing, DropdownGroup, DropdownMaster
    resumes_qs = ResumeProcessing.objects.all()

    # Only show resumes for this user (or all if superuser)
    if not request.user.is_superuser:
        resumes_qs = resumes_qs.filter(user=request.user)

    # Apply filters
    if job_filter:
        resumes_qs = resumes_qs.filter(job__title__in=job_filter)
    if resumesource_filter:
        resumes_qs = resumes_qs.filter(resumesource__id__in=resumesource_filter)
    if status_filter:
        resumes_qs = resumes_qs.filter(status__in=status_filter)

    total = resumes_qs.count()
    resumes = resumes_qs.order_by('-created_at')[offset:offset+limit]

    # For filter dropdowns
    jobs = ResumeProcessing.objects.values_list('job__title', flat=True).distinct().exclude(job__title__isnull=True).exclude(job__title='')
    try:
        resume_source_group = DropdownGroup.objects.get(text='ResumeSource', is_active=True)
        resume_sources = DropdownMaster.objects.filter(group=resume_source_group, is_active=True).order_by('sort_order', 'text')
    except DropdownGroup.DoesNotExist:
        resume_sources = []

    context = {
        'page_title': 'My Uploaded Resumes',
        'resumes': resumes,
        'total': total,
        'limit': limit,
        'offset': offset,
        'has_next': (offset + limit) < total,
        'has_prev': offset > 0,
        'next_offset': offset + limit,
        'prev_offset': max(0, offset - limit),
        'jobs': jobs,
        'resume_sources': resume_sources,
    }
    return render(request, 'Pages/RPO-Admin/resume_list.html', context)


@login_required
def rpo_resume_view(request, resume_id):
    """
    View resume details
    """
    from App.models import ResumeProcessing
    from django.http import HttpResponseForbidden
    
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        return HttpResponseForbidden('Access denied. RPO Admin role required.')
    
    try:
        resume = ResumeProcessing.objects.get(id=resume_id, user=request.user)
        context = {
            'page_title': 'View Resume',
            'resume': resume
        }
        return render(request, 'Pages/RPO-Admin/resume_view.html', context)
    except ResumeProcessing.DoesNotExist:
        messages.error(request, 'Resume not found.')
        return redirect('App:rpo_resume_list')


@login_required
def rpo_resume_download(request, resume_id):
    """
    Download resume file
    """
    from App.models import ResumeProcessing
    from django.http import FileResponse, Http404, HttpResponseForbidden
    from django.conf import settings
    import os
    
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        return HttpResponseForbidden('Access denied. RPO Admin role required.')
    
    try:
        resume = ResumeProcessing.objects.get(id=resume_id, user=request.user)
        
        # Build absolute path from relative path stored in database
        if resume.resume_path.startswith('/') or resume.resume_path.startswith('\\'):
            # Remove leading slash if present
            resume.resume_path = resume.resume_path.lstrip('/\\')
        
        absolute_path = os.path.join(settings.BASE_DIR, resume.resume_path)
        
        if not os.path.exists(absolute_path):
            messages.error(request, 'Resume file not found.')
            return redirect('App:rpo_resume_list')
        
        # Open and return the file
        response = FileResponse(open(absolute_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{resume.original_filename}"'
        return response
        
    except ResumeProcessing.DoesNotExist:
        raise Http404("Resume not found")


@login_required
@require_http_methods(["POST"])
def rpo_process_resumes(request):
    """
    Process pending resumes (extract data, analyze, store in database)
    POST: Trigger processing for pending resumes
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get specific resume IDs from request or process all pending
    resume_ids_str = request.POST.get('resume_ids', '')
    resume_ids = None
    
    if resume_ids_str:
        try:
            resume_ids = [int(id.strip()) for id in resume_ids_str.split(',') if id.strip()]
        except ValueError:
            messages.error(request, 'Invalid resume IDs format')
            return redirect(request.META.get('HTTP_REFERER', 'App:rpo_dashboard'))
    
    # Get job_id from request if provided
    job_id_str = request.POST.get('job_id', '')
    job_id = None
    
    if job_id_str:
        try:
            job_id = int(job_id_str.strip())
        except ValueError:
            messages.error(request, 'Invalid Job ID format')
            return redirect(request.META.get('HTTP_REFERER', 'App:rpo_dashboard'))
    
    # Use service to process resumes
    result = ResumeUploadService.process_pending_resumes(request.user, resume_ids, job_id)
    
    if result.success:
        messages.success(request, result.message)
        
        # Show details of processing
        if result.data['failed'] > 0:
            messages.warning(
                request, 
                f"{result.data['failed']} resume(s) failed to process. Check resume list for details."
            )
    else:
        messages.error(request, result.message)
    
    # Redirect back to referring page or dashboard
    return redirect(request.META.get('HTTP_REFERER', 'App:rpo_dashboard'))


@login_required
@require_http_methods(["POST"])
def rpo_process_single_resume(request, resume_id):
    """
    Process a single resume
    POST: Trigger processing for one specific resume
    """
    # Check if user is RPO Admin
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Use service to process single resume
    result = ResumeUploadService.process_single_resume(resume_id, request.user)
    
    if result.success:
        messages.success(request, result.message)
    else:
        messages.error(request, result.message)
    
    # Redirect back to referring page or resume view
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    from django.urls import reverse
    return redirect(reverse('App:rpo_resume_view', kwargs={'resume_id': resume_id}))


@login_required
@require_http_methods(["GET"])
def rpo_posted_jobs(request):
    """
    RPO Admin Posted Jobs List Page
    Display all posted jobs with search, filter, sort, and pagination
    GET: Display jobs table with controls
    """
    # Check if user is RPO Admin or Superuser
    user_role = request.user.profile.role if hasattr(request.user, 'profile') else 'unknown'
    is_rpo_admin = user_role == 'rpo_admin' or request.user.groups.filter(name='rpo_admin').exists()
    
    if not is_rpo_admin and not request.user.is_superuser:
        messages.error(request, 'Access denied. RPO Admin role required.')
        return redirect('App:index')
    
    # Get query parameters
    search = request.GET.get('search', '').strip()
    job_type = request.GET.get('job_type', '').strip()
    job_category = request.GET.get('job_category', '').strip()
    is_active_filter = request.GET.get('is_active', '').strip()
    sort_by = request.GET.get('sort_by', '-created_at').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    
    # Prepare filters
    filters = {}
    if job_type:
        filters['job_type'] = job_type
    if job_category:
        filters['job_category'] = job_category
    if is_active_filter:
        filters['is_active'] = is_active_filter.lower() == 'true'
    
    # Use service to get jobs
    result = JobService.get_posted_jobs_for_rpo(
        search=search,
        filters=filters,
        sort_by=sort_by,
        page=page,
        page_size=page_size
    )
    
    if result.success:
        jobs_data = result.data
        
        # Get statistics
        stats_result = JobService.get_job_statistics_api()
        stats = stats_result.data if stats_result.success else {}
        
        # Get dropdown options for filters
        from App.models import DropdownMaster
        job_types = DropdownMaster.objects.filter(
            group__value='job_type', 
            is_active=True
        ).order_by('sort_order', 'text')
        
        job_categories = DropdownMaster.objects.filter(
            group__value='job_category', 
            is_active=True
        ).order_by('sort_order', 'text')
        
        context = {
            'jobs': jobs_data['items'],
            'total_count': jobs_data.get('total_count', 0),
            'page': jobs_data.get('page', page),
            'page_size': jobs_data.get('page_size', page_size),
            'total_pages': jobs_data.get('total_pages', 1),
            'has_previous': jobs_data.get('has_previous', False),
            'has_next': jobs_data.get('has_next', False),
            'previous_page': jobs_data.get('previous_page'),
            'next_page': jobs_data.get('next_page'),
            'stats': stats,
            'job_types': job_types,
            'job_categories': job_categories,
            'search': search,
            'selected_job_type': job_type,
            'selected_job_category': job_category,
            'selected_is_active': is_active_filter,
            'sort_by': sort_by,
        }
        
        return render(request, 'Pages/RPO-Admin/posted_jobs.html', context)
    else:
        messages.error(request, result.message)
        context = {
            'jobs': [],
            'total_count': 0,
            'stats': {},
            'job_types': [],
            'job_categories': [],
        }
        return render(request, 'Pages/RPO-Admin/posted_jobs.html', context)
