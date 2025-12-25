# Quick Start Guide - Job Service Layer

## Immediate Setup (5 minutes)

### 1. Add to your main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your existing patterns ...
    path('', include('App.urls_job_management')),
]
```

### 2. Add to `settings.py`:

```python
# Job Board API Credentials (optional - for external integrations)
JOBBOARD_CREDENTIALS = {
    'indeed': {'api_key': 'your_key', 'employer_id': 'your_id'},
    'ziprecruiter': {'api_key': 'your_key', 'account_id': 'your_id'},
    'linkedin': {'client_id': 'your_id', 'client_secret': 'your_secret'},
    'jobelephant': {'api_key': 'your_key', 'partner_id': 'your_id'}
}

# Email for job applications
JOB_APPLICATION_EMAIL = 'jobs@yourcompany.com'
```

### 3. Use in your code:

**In Django Templates (MVT):**
```python
from App.services import job_service

# In your view
def my_view(request):
    result = job_service.search_jobs(
        search_query='python',
        page=1,
        per_page=20
    )
    return render(request, 'template.html', {'jobs': result['data']})
```

**In REST API:**
```python
from App.services import job_service
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def jobs_api(request):
    result = job_service.search_jobs(page=1, per_page=20)
    return Response(result)
```

## Common Tasks

### Create a Job
```python
from App.services import job_service

result = job_service.create_job_post(
    data={'title': 'Developer', 'job_summary': 'Looking for...'},
    user=request.user,
    publish_to_boards=['indeed', 'linkedin']  # Optional
)
```

### Search Jobs
```python
result = job_service.search_jobs(
    search_query='python',
    filters={'job_type': 'full_time', 'location': 'New York'},
    page=1,
    per_page=20
)

jobs = result['data']
```

### Handle Application
```python
from App.services import application_service

result = application_service.submit_application(
    job_id=123,
    applicant_data={'name': 'John', 'email': 'john@example.com'},
    resume_file=request.FILES['resume']
)
```

## Available URLs

### Public Pages
- `/jobs/` - Job listing
- `/jobs/123/` - Job detail
- `/jobs/123/apply/` - Apply to job

### Employer Pages
- `/employer/dashboard/` - Employer dashboard
- `/employer/jobs/create/` - Create job
- `/employer/jobs/123/edit/` - Edit job
- `/employer/jobs/123/applications/` - View applications

### API Endpoints
- `GET /api/jobs/` - List jobs
- `POST /api/jobs/create/` - Create job
- `POST /api/jobs/apply/` - Submit application
- `GET /api/jobs/123/applications/` - Get applications

**See full documentation in `JOB_SERVICE_LAYER_DOCUMENTATION.md`**

## Testing

```python
# Test in Django shell
python manage.py shell

from App.services import job_service
from django.contrib.auth.models import User

user = User.objects.first()
result = job_service.create_job_post(
    data={'title': 'Test Job', 'job_summary': 'Testing...'},
    user=user
)
print(result)
```

That's it! You're ready to go! 🚀
