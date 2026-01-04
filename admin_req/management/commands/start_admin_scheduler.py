import os
from dotenv import load_dotenv
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import time
import threading

load_dotenv()

SCHEDULE_TIME = os.getenv('ADMIN_REQ_SCHEDULE_TIME', '07:00')  # Format: HH:MM
API_URL = os.getenv('ADMIN_REQ_BULK_RESUME_API', 'http://localhost:8000/api/zoho/bulk-resume-download/')
API_USERNAME = os.getenv('ADMIN_REQ_API_USERNAME', 'admin')
API_PASSWORD = os.getenv('ADMIN_REQ_API_PASSWORD', 'admin')


def call_bulk_resume_download():
    """
    Calls the bulk resume download API endpoint with basic authentication.
    """
    try:
        print(f"[admin_req] Calling API: {API_URL}")
        response = requests.post(API_URL, auth=(API_USERNAME, API_PASSWORD))
        print(f"[admin_req] API Response: {response.status_code} {response.content}")
    except Exception as e:
        print(f"[admin_req] Error calling API: {e}")


def scheduler_loop():
    """
    Scheduler loop that runs the API call daily at the scheduled time.
    """
    while True:
        now = timezone.localtime()
        target_time = datetime.strptime(SCHEDULE_TIME, '%H:%M').time()
        next_run = now.replace(hour=target_time.hour, minute=target_time.minute, second=0, microsecond=0)
        if now.time() > target_time:
            # If time has passed today, schedule for tomorrow
            next_run = next_run + timedelta(days=1)
        sleep_seconds = (next_run - now).total_seconds()
        print(f"[admin_req] Sleeping for {sleep_seconds} seconds until next run at {next_run}")
        if sleep_seconds > 0:
            time.sleep(0)
        call_bulk_resume_download()
        # Sleep for 24 hours after running
        time.sleep(24 * 60 * 60)


class Command(BaseCommand):
    help = 'Starts the admin_req scheduler to run bulk resume download daily.'

    def handle(self, *args, **options):
        print("[admin_req] Scheduler started.")
        t = threading.Thread(target=scheduler_loop, daemon=True)
        t.start()
        # Keep the management command running
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("[admin_req] Scheduler stopped.")
