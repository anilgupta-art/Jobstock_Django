"""
Quick Script: Clean All Resume Data
Deletes all ResumeProcessing, ResumeJobMatch, and related candidate data
Usage: python manage.py shell < clean_all_resume_data.py
"""
from django.db import transaction
from App.models import (
    ResumeProcessing,
    ResumeJobMatch,
    CandidateSkill,
    CandidateEducation,
    CandidateExperience,
    CandidateCertification,
    ErrorLog
)
import os
from django.conf import settings

print("\n" + "="*80)
print("RESUME DATA CLEANUP SCRIPT")
print("="*80)

# Count current records
resume_count = ResumeProcessing.objects.count()
match_count = ResumeJobMatch.objects.count()
skill_count = CandidateSkill.objects.count()
education_count = CandidateEducation.objects.count()
experience_count = CandidateExperience.objects.count()
certification_count = CandidateCertification.objects.count()

print(f"\n📊 Current Database State:")
print(f"   • ResumeProcessing records: {resume_count}")
print(f"   • ResumeJobMatch records: {match_count}")
print(f"   • CandidateSkill records: {skill_count}")
print(f"   • CandidateEducation records: {education_count}")
print(f"   • CandidateExperience records: {experience_count}")
print(f"   • CandidateCertification records: {certification_count}")

total_records = resume_count + match_count + skill_count + education_count + experience_count + certification_count

if total_records == 0:
    print("\n✓ Database is already clean. No records to delete.")
else:
    print(f"\n   TOTAL TO DELETE: {total_records} records")
    print("\n⚠️  WARNING: This will delete ALL resume-related data!")
    print("="*80)
    
    try:
        with transaction.atomic():
            deleted_counts = {}
            
            # Delete in proper order (child records first)
            print("\nDeleting records...")
            
            if skill_count > 0:
                result = CandidateSkill.objects.all().delete()
                deleted_counts['skills'] = result[0]
                print(f"✓ Deleted {result[0]} candidate skills")
            
            if education_count > 0:
                result = CandidateEducation.objects.all().delete()
                deleted_counts['education'] = result[0]
                print(f"✓ Deleted {result[0]} candidate education records")
            
            if experience_count > 0:
                result = CandidateExperience.objects.all().delete()
                deleted_counts['experience'] = result[0]
                print(f"✓ Deleted {result[0]} candidate experience records")
            
            if certification_count > 0:
                result = CandidateCertification.objects.all().delete()
                deleted_counts['certifications'] = result[0]
                print(f"✓ Deleted {result[0]} candidate certifications")
            
            if match_count > 0:
                result = ResumeJobMatch.objects.all().delete()
                deleted_counts['matches'] = result[0]
                print(f"✓ Deleted {result[0]} resume-job matches")
            
            if resume_count > 0:
                result = ResumeProcessing.objects.all().delete()
                deleted_counts['resumes'] = result[0]
                print(f"✓ Deleted {result[0]} resume processing records")
            
            # Delete resume-related error logs
            error_result = ErrorLog.objects.filter(
                error_type__in=['resume_processing', 'resume_extraction', 'resume_matching']
            ).delete()
            if error_result[0] > 0:
                deleted_counts['error_logs'] = error_result[0]
                print(f"✓ Deleted {error_result[0]} error log entries")
        
        print("\n" + "="*80)
        print("✅ DATABASE CLEANUP COMPLETED SUCCESSFULLY!")
        print("="*80)
        print(f"\nTotal records deleted: {sum(deleted_counts.values())}")
        
        # Check for physical files
        resume_dir = os.path.join(settings.BASE_DIR, 'Data', 'resume')
        if os.path.exists(resume_dir):
            file_count = sum(len(files) for _, _, files in os.walk(resume_dir))
            print(f"\n📁 Physical Resume Files:")
            print(f"   Location: {resume_dir}")
            print(f"   Files remaining: {file_count}")
            print("\n   To delete physical files, run:")
            print("   python manage.py clean_resume_data --delete-files")
        
        # Verify deletion
        print("\n🔍 Verification:")
        print(f"   • ResumeProcessing: {ResumeProcessing.objects.count()} (should be 0)")
        print(f"   • ResumeJobMatch: {ResumeJobMatch.objects.count()} (should be 0)")
        print(f"   • CandidateSkill: {CandidateSkill.objects.count()} (should be 0)")
        print(f"   • CandidateEducation: {CandidateEducation.objects.count()} (should be 0)")
        print(f"   • CandidateExperience: {CandidateExperience.objects.count()} (should be 0)")
        print(f"   • CandidateCertification: {CandidateCertification.objects.count()} (should be 0)")
        
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Transaction rolled back. No changes made.")
        print("="*80 + "\n")
