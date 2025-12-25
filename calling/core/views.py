from django.http import HttpResponse
from django.urls import reverse

def home(request):
    html = f'''
    <h2>Welcome to the Online Video Calling System</h2>
    <ul>
        <li><a href="/admin/">Admin Panel</a></li>
        <li><a href="/video_call_test.html">Video Call Test Page</a></li>
        <li><a href="/api/video/upload/1/">Upload Video Recording (API, POST)</a></li>
        <li><a href="/api/questions/generate/1/">Generate Questions (API, POST)</a></li>
        <li><a href="/media/">View Recordings (media folder)</a></li>
    </ul>
    <p>See the README for API usage details.</p>
    '''
    return HttpResponse(html)
