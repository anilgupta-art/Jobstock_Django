"""
Test script to verify job-specific resume processing
Usage: python manage.py shell < test_job_filter_processing.py
"""
from django.contrib.auth.models import User
from App.models import ResumeProcessing, Job
from App.services.resume_upload_service import ResumeUploadService

print("\n" + "="*70)
print("Testing Job-Filtered Resume Processing")
print("="*70)

# Get RPO admin user
try:
    rpo_user = User.objects.filter(groups__name='rpo_admin').first()
    if not rpo_user:
        rpo_user = User.objects.filter(is_superuser=True).first()
    
    if not rpo_user:
        print("❌ No RPO admin or superuser found")
        exit()
    
    print(f"\n✓ Using user: {rpo_user.username}")
except Exception as e:
    print(f"❌ Error getting user: {e}")
    exit()

# Get total pending resumes
total_pending = ResumeProcessing.objects.filter(
    user=rpo_user,
    status='pending'
).count()

print(f"✓ Total pending resumes: {total_pending}")

# Get jobs with pending resumes
jobs_with_resumes = ResumeProcessing.objects.filter(
    user=rpo_user,
    status='pending',
    job__isnull=False
).values_list('job_id', flat=True).distinct()

print(f"✓ Jobs with pending resumes: {list(jobs_with_resumes)}")

# Test 1: Process all pending (no job_id filter)
print("\n" + "-"*70)
print("Test 1: Process ALL pending resumes (no job_id)")
print("-"*70)

result = ResumeUploadService.process_pending_resumes(
    user=rpo_user,
    resume_ids=None,
    job_id=None
)

print(f"Success: {result.success}")
print(f"Message: {result.message}")
print(f"Data: {result.data}")

# Test 2: Process resumes for specific job (if job exists)
if jobs_with_resumes:
    test_job_id = list(jobs_with_resumes)[0]
    
    print("\n" + "-"*70)
    print(f"Test 2: Process resumes for Job ID {test_job_id}")
    print("-"*70)
    
    # Count pending for this job
    job_pending = ResumeProcessing.objects.filter(
        user=rpo_user,
        status='pending',
        job_id=test_job_id
    ).count()
    
    print(f"✓ Pending resumes for Job {test_job_id}: {job_pending}")
    
    result = ResumeUploadService.process_pending_resumes(
        user=rpo_user,
        resume_ids=None,
        job_id=test_job_id
    )
    
    print(f"Success: {result.success}")
    print(f"Message: {result.message}")
    print(f"Data: {result.data}")
else:
    print("\n⚠ No jobs with pending resumes to test job-specific filtering")

# Test 3: Process with invalid job_id
print("\n" + "-"*70)
print("Test 3: Process with non-existent job_id")
print("-"*70)

result = ResumeUploadService.process_pending_resumes(
    user=rpo_user,
    resume_ids=None,
    job_id=99999  # Non-existent job
)

print(f"Success: {result.success}")
print(f"Message: {result.message}")
print(f"Data: {result.data}")

print("\n" + "="*70)
print("Testing Complete!")
print("="*70)
print("\n📋 USAGE EXAMPLES:")
print("-"*70)
print("1. Process ALL pending resumes:")
print("   http://127.0.0.1:8000/rpo-dashboard/")
print("   Click 'Process All Pending'")
print()
print("2. Process resumes for specific job:")
print("   http://127.0.0.1:8000/rpo-dashboard/?job_id=123")
print("   Click 'Process All Pending'")
print("   (Only processes resumes for Job ID 123)")
print()
print("3. In templates, add job filter:")
print('   <a href="{% url \'App:rpo_dashboard\' %}?job_id={{ job.id }}">')
print("   Process Job {{ job.id }} Resumes</a>")
print("="*70 + "\n")
