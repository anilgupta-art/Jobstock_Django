"""
Forms Package
"""

from .job_forms import *
from .candidate_forms import *

__all__ = [
    # Job forms
    'JobPostForm',
    'JobSearchForm',
    'JobApplicationForm',
    'ApplicationStatusForm',
    # Candidate forms
    'SignUpForm',
    'CandidateProfileBasicForm',
    'CandidateProfileContactForm',
    'CandidateProfileSocialForm',
    'CandidateResumeForm',
    'CandidateSkillForm',
    'CandidateEducationForm',
    'CandidateExperienceForm',
    'CandidateCertificationForm',
    'RoleAssignForm',
]
