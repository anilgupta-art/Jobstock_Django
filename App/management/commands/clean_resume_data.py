"""
Management Command: Clean Resume Processing Data
Deletes all resume processing, matching, and related data
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
import os
import shutil
from App.models import (
    ResumeProcessing,
    ResumeJobMatch,
    CandidateSkill,
    CandidateEducation,
    CandidateExperience,
    CandidateCertification,
    ErrorLog
)


class Command(BaseCommand):
    help = 'Clean all resume processing data (ResumeProcessing, ResumeJobMatch, and related records)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting',
        )
        parser.add_argument(
            '--delete-files',
            action='store_true',
            help='Also delete physical resume files from disk',
        )
        parser.add_argument(
            '--keep-files',
            action='store_true',
            help='Keep physical files, only delete database records',
        )

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*80)
        self.stdout.write(self.style.WARNING("RESUME DATA CLEANUP UTILITY"))
        self.stdout.write("="*80 + "\n")

        # Count records to delete
        resume_count = ResumeProcessing.objects.count()
        match_count = ResumeJobMatch.objects.count()
        skill_count = CandidateSkill.objects.count()
        education_count = CandidateEducation.objects.count()
        experience_count = CandidateExperience.objects.count()
        certification_count = CandidateCertification.objects.count()
        error_log_count = ErrorLog.objects.filter(
            error_type__in=['resume_processing', 'resume_extraction', 'resume_matching']
        ).count()

        self.stdout.write("📊 Records to be deleted:")
        self.stdout.write(f"   • ResumeProcessing: {resume_count}")
        self.stdout.write(f"   • ResumeJobMatch: {match_count}")
        self.stdout.write(f"   • CandidateSkill: {skill_count}")
        self.stdout.write(f"   • CandidateEducation: {education_count}")
        self.stdout.write(f"   • CandidateExperience: {experience_count}")
        self.stdout.write(f"   • CandidateCertification: {certification_count}")
        self.stdout.write(f"   • ErrorLog (resume-related): {error_log_count}")
        self.stdout.write(f"\n   TOTAL: {resume_count + match_count + skill_count + education_count + experience_count + certification_count + error_log_count} records\n")

        # Check for resume files
        resume_dir = os.path.join(settings.BASE_DIR, 'Data', 'resume')
        resume_files_exist = os.path.exists(resume_dir)
        
        if resume_files_exist:
            # Count files
            file_count = 0
            total_size = 0
            for root, dirs, files in os.walk(resume_dir):
                file_count += len(files)
                total_size += sum(os.path.getsize(os.path.join(root, f)) for f in files)
            
            self.stdout.write(f"📁 Physical resume files:")
            self.stdout.write(f"   • Location: {resume_dir}")
            self.stdout.write(f"   • Files: {file_count}")
            self.stdout.write(f"   • Size: {total_size / (1024*1024):.2f} MB\n")

        if resume_count == 0 and match_count == 0:
            self.stdout.write(self.style.SUCCESS("✓ No resume data found. Database is already clean."))
            return

        # Confirmation
        if not options['confirm']:
            self.stdout.write(self.style.WARNING("\n⚠️  WARNING: This action cannot be undone!"))
            confirm = input("\nType 'DELETE' to confirm: ")
            if confirm != 'DELETE':
                self.stdout.write(self.style.ERROR("✗ Cleanup cancelled."))
                return

        # Ask about files if not specified
        delete_files = False
        if resume_files_exist and not options['keep_files']:
            if options['delete_files']:
                delete_files = True
            else:
                file_confirm = input("\nDelete physical resume files too? (yes/no): ")
                delete_files = file_confirm.lower() in ['yes', 'y']

        self.stdout.write("\n" + "-"*80)
        self.stdout.write("Starting cleanup...")
        self.stdout.write("-"*80 + "\n")

        try:
            with transaction.atomic():
                # Delete in proper order (child tables first)
                
                # 1. Delete error logs
                if error_log_count > 0:
                    deleted_errors = ErrorLog.objects.filter(
                        error_type__in=['resume_processing', 'resume_extraction', 'resume_matching']
                    ).delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_errors[0]} error log entries"
                    ))

                # 2. Delete candidate data (linked to ResumeProcessing)
                if skill_count > 0:
                    deleted_skills = CandidateSkill.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_skills[0]} candidate skills"
                    ))

                if education_count > 0:
                    deleted_education = CandidateEducation.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_education[0]} candidate education records"
                    ))

                if experience_count > 0:
                    deleted_experience = CandidateExperience.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_experience[0]} candidate experience records"
                    ))

                if certification_count > 0:
                    deleted_certs = CandidateCertification.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_certs[0]} candidate certifications"
                    ))

                # 3. Delete resume job matches
                if match_count > 0:
                    deleted_matches = ResumeJobMatch.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_matches[0]} resume-job matches"
                    ))

                # 4. Delete resume processing records
                if resume_count > 0:
                    deleted_resumes = ResumeProcessing.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted {deleted_resumes[0]} resume processing records"
                    ))

            self.stdout.write(self.style.SUCCESS("\n✓ Database cleanup completed successfully!"))

            # Delete physical files if requested
            if delete_files and resume_files_exist:
                self.stdout.write("\n" + "-"*80)
                self.stdout.write("Deleting physical resume files...")
                self.stdout.write("-"*80 + "\n")
                
                try:
                    shutil.rmtree(resume_dir)
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ Deleted resume directory: {resume_dir}"
                    ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f"✗ Error deleting files: {str(e)}"
                    ))
            elif resume_files_exist:
                self.stdout.write(self.style.WARNING(
                    f"\n⚠️  Physical files kept at: {resume_dir}"
                ))
                self.stdout.write("   Run with --delete-files to remove them.")

            # Summary
            self.stdout.write("\n" + "="*80)
            self.stdout.write(self.style.SUCCESS("CLEANUP SUMMARY"))
            self.stdout.write("="*80)
            self.stdout.write(f"✓ Database records deleted: {resume_count + match_count + skill_count + education_count + experience_count + certification_count + error_log_count}")
            if delete_files:
                self.stdout.write(f"✓ Physical files deleted: {file_count} files ({total_size / (1024*1024):.2f} MB)")
            self.stdout.write("="*80 + "\n")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"\n✗ Error during cleanup: {str(e)}"))
            self.stdout.write(self.style.ERROR("Transaction rolled back. No changes made."))
