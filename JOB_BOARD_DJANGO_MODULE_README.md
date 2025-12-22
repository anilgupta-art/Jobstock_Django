# Job Board Integration - Django Module

## ✅ Complete Django Module Structure

The job board integration has been converted into a **fully maintainable Django module** with proper Django patterns.

## 📦 Module Components

### 1. **Models** (`App/models/job_board_models.py`)

Three Django models for complete tracking:

- **`JobBoardMapping`** - Tracks jobs posted to external boards
  - Links internal jobs to external board IDs
  - Tracks status (active, paused, closed, error)
  - Metrics (views, applications)
  - Error tracking with retry capability

- **`ExternalApplication`** - Stores applications from boards
  - Candidate information
  - Resume storage
  - Application status tracking
  - Internal notes

- **`BoardSyncLog`** - Audit log for all board operations
  - Request/response tracking
  - Performance metrics
  - Error debugging

### 2. **Django Admin** (`App/admin/job_board_admin.py`)

Beautiful, functional admin interface with:

- **Colored badges** for status, boards, and actions
- **Bulk actions** - Sync, close, retry failed
- **Search & filters** by board, status, date
- **JSON viewers** for API request/response data
- **Quick links** between related records

### 3. **Management Commands**

#### `python manage.py sync_jobs_to_boards`
```bash
# Sync all jobs
python manage.py sync_jobs_to_boards --all

# Sync specific job
python manage.py sync_jobs_to_boards --job-id 123

# Sync to specific board
python manage.py sync_jobs_to_boards --board indeed --active-only

# Retry failed postings
python manage.py sync_jobs_to_boards --retry-failed

# Dry run to see what would happen
python manage.py sync_jobs_to_boards --all --dry-run
```

#### `python manage.py fetch_external_applications`
```bash
# Fetch for all jobs
python manage.py fetch_external_applications --all

# Fetch for specific job
python manage.py fetch_external_applications --job-id 123

# Fetch from specific board only
python manage.py fetch_external_applications --all --board indeed
```

### 4. **Django Signals** (`App/signals/job_board_signals.py`)

Automatic integration via signals:

- **`post_save(Job)`** - Auto-publish new jobs to boards
- **`post_save(Job)`** - Auto-sync job updates to boards
- **`pre_delete(Job)`** - Auto-remove from boards before deletion

### 5. **Configuration** (`App/conf/job_board_settings.py`)

Centralized settings management:

```python
# Copy to your settings.py

JOBBOARD_CREDENTIALS = {
    'indeed': {'api_key': '...'},
    'ziprecruiter': {'api_key': '...'},
    'linkedin': {'client_id': '...', 'client_secret': '...'},
    'jobelephant': {'api_key': '...'},
}

AUTO_PUBLISH_JOBS_TO_BOARDS = False  # Enable auto-posting
AUTO_SYNC_JOB_UPDATES = False         # Enable auto-sync
AUTO_REMOVE_JOBS_FROM_BOARDS = True   # Auto-remove on delete

DEFAULT_JOB_BOARDS = ['indeed', 'ziprecruiter']  # Default boards
```

## 🚀 Setup Instructions

### Step 1: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 2: Configure Settings

Add to `Jobstock/settings.py`:

```python
# Import job board settings
from App.conf.job_board_settings import *

# Or manually add:
JOBBOARD_CREDENTIALS = {
    'indeed': {
        'api_key': 'your_key',
        'employer_id': 'your_id',
    },
    # ... other boards
}
```

### Step 3: Enable Signals (Already Done)

The `App/apps.py` now automatically loads signals.

### Step 4: Access Django Admin

```bash
python manage.py runserver
# Visit http://localhost:8000/admin/
```

You'll see:
- **Job Board Mappings** - Manage external postings
- **External Applications** - Review applications
- **Board Sync Logs** - Audit trail

## 💡 Usage Examples

### Programmatic Usage

```python
from App.services import job_board_service
from App.models.job_board_models import JobBoardMapping

# Post job to boards
result = job_board_service.publish_to_multiple_boards(
    job_id=123,
    boards=['indeed', 'ziprecruiter', 'linkedin']
)

# Check mappings
mappings = JobBoardMapping.objects.filter(job_id=123)
for mapping in mappings:
    print(f"{mapping.get_board_display()}: {mapping.status}")

# Sync updates
job_board_service.sync_job_updates(job_id=123)

# Fetch applications
apps = job_board_service.fetch_applications(job_id=123)
```

### Admin Interface Usage

1. **Post a job**:
   - Create job in Django admin
   - Click "Save and continue editing"
   - JobBoardMapping records auto-created
   
2. **Monitor status**:
   - Visit "Job Board Mappings"
   - See colored status badges
   - View metrics (views, applications)

3. **Handle errors**:
   - Filter by "Error" status
   - Select failed mappings
   - Choose "Retry failed postings" action

4. **Review applications**:
   - Visit "External Applications"
   - Filter by source board
   - Bulk actions: Review, Shortlist, Reject

### Automated Workflow (Signals)

Enable in settings:
```python
AUTO_PUBLISH_JOBS_TO_BOARDS = True
DEFAULT_JOB_BOARDS = ['indeed', 'ziprecruiter']
```

Then:
```python
# Just create a job - it auto-posts!
job = Job.objects.create(
    title="Senior Developer",
    # ... other fields
)
# ✅ Automatically posted to Indeed & ZipRecruiter
# ✅ JobBoardMapping records created
# ✅ All logged in BoardSyncLog
```

## 🎯 Benefits of Django Module Approach

### ✅ Maintainability
- **Proper Django models** - ORM, migrations, relationships
- **Admin interface** - No custom UI needed
- **Management commands** - Easy CLI operations
- **Signals** - Automatic integration

### ✅ Monitoring
- **Complete audit trail** - BoardSyncLog tracks everything
- **Error tracking** - Automatic retry counts and timestamps
- **Metrics** - View counts, application counts per board
- **Admin filters** - Find issues quickly

### ✅ Flexibility
- **Enable/disable** auto-posting via settings
- **Per-board control** - Post to specific boards only
- **Dry run mode** - Test without actual posting
- **Bulk operations** - Handle multiple jobs at once

### ✅ Production Ready
- **Transaction safety** - Database integrity guaranteed
- **Logging** - Structured logs for debugging
- **Error handling** - Graceful failures with retry
- **Performance** - Database queries optimized

## 📊 Database Schema

```
job_board_mapping
├── job (FK → Job)
├── board (indeed/ziprecruiter/linkedin/jobelephant)
├── external_job_id
├── status (pending/active/paused/closed/error)
├── view_count
├── application_count
└── timestamps...

external_application
├── job (FK → Job)
├── board_mapping (FK → JobBoardMapping)
├── candidate_name, email, phone
├── resume_url, resume_file
├── source (board name)
├── status (new/reviewed/shortlisted/rejected/hired)
└── timestamps...

board_sync_log
├── job (FK → Job)
├── board_mapping (FK → JobBoardMapping)
├── action (post/update/close/fetch_apps)
├── status (success/error/partial)
├── request_data (JSON)
├── response_data (JSON)
└── duration_seconds
```

## 🔧 Next Steps

1. **Run migrations** to create tables
2. **Configure API credentials** in settings
3. **Test in Django admin** - create/edit jobs
4. **Enable signals** for automation
5. **Monitor BoardSyncLog** for issues
6. **Schedule periodic syncs** via cron/celery

---

**The job board integration is now a fully maintainable Django module!** 🎉
