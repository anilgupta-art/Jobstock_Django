"""
Configuration Module for Job Board Integration
Add this to your settings.py
"""

# Job Board Integration Settings

# API Credentials for external job boards
JOBBOARD_CREDENTIALS = {
    'indeed': {
        'api_key': 'your_indeed_api_key',
        'employer_id': 'your_indeed_employer_id',
        'publisher_id': 'your_publisher_id',
    },
    'ziprecruiter': {
        'api_key': 'your_ziprecruiter_api_key',
        'account_id': 'your_account_id',
    },
    'linkedin': {
        'client_id': 'your_linkedin_client_id',
        'client_secret': 'your_linkedin_client_secret',
        'access_token': 'your_linkedin_access_token',
    },
    'jobelephant': {
        'api_key': 'your_jobelephant_api_key',
        'partner_id': 'your_partner_id',
    }
}

# Email for receiving applications
JOB_APPLICATION_EMAIL = 'jobs@yourcompany.com'

# Auto-publish settings
AUTO_PUBLISH_JOBS_TO_BOARDS = False  # Set to True to auto-publish on job creation
AUTO_SYNC_JOB_UPDATES = False  # Set to True to auto-sync job updates
AUTO_REMOVE_JOBS_FROM_BOARDS = True  # Auto-remove from boards when job is deleted

# Default boards to publish to (when AUTO_PUBLISH_JOBS_TO_BOARDS is True)
DEFAULT_JOB_BOARDS = [
    # 'indeed',
    # 'ziprecruiter',
    # 'linkedin',
    # 'jobelephant',
]

# Logging configuration for job board integration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'job_board_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/job_board_integration.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'loggers': {
        'App.services.job_board_integration_service': {
            'handlers': ['job_board_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'App.signals.job_board_signals': {
            'handlers': ['job_board_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
