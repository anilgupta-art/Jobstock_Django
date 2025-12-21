"""
Test Resume-Job Matching System
Demonstrates AI-powered matching with detailed analysis
"""
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jobstock.settings')
django.setup()

from App.models import Job, ResumeProcessing, ResumeJobMatch
from App.services.resume_matching_service import ResumeJobMatchingService
from App.tasks_matching import match_resume_to_job_task, match_resume_to_all_jobs_task


def test_single_match():
    """Test matching a single resume to a job"""
    print("="*80)
    print("TEST 1: SINGLE RESUME-JOB MATCH")
    print("="*80)
    
    # Get first completed resume and active job
    resume = ResumeProcessing.objects.filter(status='completed').first()
    job = Job.objects.filter(is_active=True).first()
    
    if not resume:
        print("❌ No completed resumes found. Please process some resumes first.")
        return
    
    if not job:
        print("❌ No active jobs found.")
        return
    
    print(f"\n📄 Resume: {resume.user.username} - {resume.original_filename}")
    print(f"   Skills: {resume.extracted_skills or 'N/A'}")
    print(f"   Experience: {resume.years_of_experience or 'N/A'}")
    print(f"   Sentiment: {resume.sentiment_score or 'N/A'}")
    
    print(f"\n💼 Job: {job.title}")
    print(f"   Category: {job.job_category}")
    print(f"   Required Skills: {job.skills or 'N/A'}")
    print(f"   Experience: {job.experience_required}")
    
    print(f"\n🔄 Calculating match...")
    
    result = ResumeJobMatchingService.match_resume_to_job(job.id, resume.id)
    
    if result.success:
        print(f"\n✅ MATCH COMPLETED")
        print(f"\n📊 Match Statistics:")
        print(f"   Overall Match: {result.data['overall_match']}%")
        print(f"   Match Quality: {result.data['match_quality'].upper()}")
        print(f"   Recommended: {'Yes' if result.data['is_recommended'] else 'No'}")
        
        print(f"\n✅ Success Reasons:")
        for reason in result.data['success_reasons']:
            print(f"   • {reason}")
        
        if result.data['failure_reasons']:
            print(f"\n❌ Failure Reasons:")
            for reason in result.data['failure_reasons']:
                print(f"   • {reason}")
        
        # Get full match object
        match = ResumeJobMatch.objects.get(id=result.data['match_id'])
        print(f"\n💡 Improvement Suggestions:")
        for suggestion in match.improvement_suggestions or []:
            print(f"   • {suggestion}")
        
        print(f"\n🔍 Detailed Breakdown:")
        print(f"   Skills Match: {match.skills_match_percentage}%")
        print(f"   Experience Match: {match.experience_match_percentage}%")
        print(f"   Location Match: {match.location_match_percentage}%")
        print(f"   Qualification Match: {match.qualification_match_percentage}%")
        
        if match.matching_skills:
            print(f"\n✓ Matching Skills ({len(match.matching_skills)}):")
            print(f"   {', '.join(match.matching_skills[:10])}")
        
        if match.missing_skills:
            print(f"\n✗ Missing Skills ({len(match.missing_skills)}):")
            print(f"   {', '.join(match.missing_skills[:10])}")
    
    else:
        print(f"\n❌ Match failed: {result.message}")


def test_batch_match():
    """Test matching one resume to all jobs"""
    print(f"\n{'='*80}")
    print("TEST 2: BATCH MATCHING (Resume to All Jobs)")
    print("="*80)
    
    resume = ResumeProcessing.objects.filter(status='completed').first()
    
    if not resume:
        print("❌ No completed resumes found.")
        return
    
    active_jobs_count = Job.objects.filter(is_active=True).count()
    
    print(f"\n📄 Resume: {resume.user.username}")
    print(f"   Skills: {resume.extracted_skills or 'N/A'[:50]}")
    print(f"\n💼 Active Jobs: {active_jobs_count}")
    
    print(f"\n🔄 Matching resume to all active jobs...")
    
    result = ResumeJobMatchingService.match_resume_to_all_jobs(resume.id)
    
    if result.success:
        total = result.data['total_jobs_matched']
        print(f"\n✅ BATCH MATCH COMPLETED")
        print(f"   Total Jobs Matched: {total}")
        
        # Get top 5 matches
        top_matches = ResumeJobMatch.objects.filter(
            resume=resume
        ).order_by('-overall_match_percentage')[:5]
        
        print(f"\n🏆 TOP 5 MATCHES:")
        for i, match in enumerate(top_matches, 1):
            print(f"\n   {i}. {match.job.title}")
            print(f"      Match: {match.overall_match_percentage}% ({match.match_quality})")
            print(f"      Recommended: {'Yes' if match.is_recommended else 'No'}")
            print(f"      Skills Match: {match.skills_match_percentage}%")
    else:
        print(f"\n❌ Batch match failed: {result.message}")


def test_background_task():
    """Test background task for matching"""
    print(f"\n{'='*80}")
    print("TEST 3: BACKGROUND TASK (Celery)")
    print("="*80)
    
    resume = ResumeProcessing.objects.filter(status='completed').first()
    job = Job.objects.filter(is_active=True).first()
    
    if not resume or not job:
        print("❌ Insufficient data for test.")
        return
    
    print(f"\n📄 Resume: {resume.user.username}")
    print(f"💼 Job: {job.title}")
    
    print(f"\n🔄 Queuing background task...")
    
    try:
        # Try to queue task
        task = match_resume_to_job_task.delay(job.id, resume.id)
        print(f"\n✅ Task queued successfully")
        print(f"   Task ID: {task.id}")
        print(f"   Status: {task.status}")
        print(f"\n⏳ Note: Task will process in background via Celery worker")
    except Exception as e:
        print(f"\n⚠️  Celery not running (this is OK for testing)")
        print(f"   Error: {str(e)}")
        print(f"\n   You can still use synchronous matching via service layer")


def show_statistics():
    """Show overall matching statistics"""
    print(f"\n{'='*80}")
    print("MATCHING SYSTEM STATISTICS")
    print("="*80)
    
    total_matches = ResumeJobMatch.objects.count()
    completed_matches = ResumeJobMatch.objects.filter(status='completed').count()
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Total Matches: {total_matches}")
    print(f"   Completed: {completed_matches}")
    print(f"   Pending: {ResumeJobMatch.objects.filter(status='pending').count()}")
    print(f"   Failed: {ResumeJobMatch.objects.filter(status='failed').count()}")
    
    if completed_matches > 0:
        print(f"\n🎯 Match Quality Distribution:")
        for quality in ['excellent', 'good', 'fair', 'poor']:
            count = ResumeJobMatch.objects.filter(
                status='completed',
                match_quality=quality
            ).count()
            percentage = (count / completed_matches * 100) if completed_matches > 0 else 0
            print(f"   {quality.capitalize()}: {count} ({percentage:.1f}%)")
        
        recommended = ResumeJobMatch.objects.filter(
            status='completed',
            is_recommended=True
        ).count()
        print(f"\n⭐ Recommended Matches: {recommended} ({recommended/completed_matches*100:.1f}%)")
        
        # Average scores
        from django.db.models import Avg
        averages = ResumeJobMatch.objects.filter(status='completed').aggregate(
            avg_overall=Avg('overall_match_percentage'),
            avg_skills=Avg('skills_match_percentage'),
            avg_experience=Avg('experience_match_percentage')
        )
        
        print(f"\n📈 Average Scores:")
        print(f"   Overall Match: {averages['avg_overall']:.2f}%")
        print(f"   Skills Match: {averages['avg_skills']:.2f}%")
        print(f"   Experience Match: {averages['avg_experience']:.2f}%")


def main():
    print("="*80)
    print("RESUME-JOB MATCHING SYSTEM TEST SUITE")
    print("="*80)
    
    # Check data availability
    resumes_count = ResumeProcessing.objects.filter(status='completed').count()
    jobs_count = Job.objects.filter(is_active=True).count()
    
    print(f"\n📋 Data Availability:")
    print(f"   Completed Resumes: {resumes_count}")
    print(f"   Active Jobs: {jobs_count}")
    
    if resumes_count == 0:
        print(f"\n❌ No completed resumes found!")
        print(f"   Please upload and process some resumes first.")
        print(f"   URL: http://127.0.0.1:8000/rpo-resume-upload/")
        return
    
    if jobs_count == 0:
        print(f"\n❌ No active jobs found!")
        print(f"   Please create some job postings first.")
        return
    
    # Run tests
    test_single_match()
    test_batch_match()
    test_background_task()
    show_statistics()
    
    print(f"\n{'='*80}")
    print("✅ TEST SUITE COMPLETE")
    print("="*80)
    print(f"\n📝 Next Steps:")
    print(f"   1. View matches in Django admin: http://127.0.0.1:8000/admin/")
    print(f"   2. Access via REST API (create views)")
    print(f"   3. Build UI templates for matching results")
    print(f"   4. Start Celery worker for background processing:")
    print(f"      celery -A Jobstock worker -l info")
    print()


if __name__ == "__main__":
    main()
