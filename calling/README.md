# Online Video Calling System (Django)

This project is licensed under the MIT License (see LICENSE file).

## Features
- Modular Django apps: users, calls, video, questions, analytics
- Human-to-human and human-to-AI video calls
- AI/ML auto-generated questions after calls
- Video recording and storage
- Django Channels for WebRTC signaling
- Django REST Framework for APIs

## Requirements
- Python 3.8+
- Django
- djangorestframework
- channels
- channels_redis
- opencv-python
- Pillow
- numpy
- scikit-learn
- openai (optional, for advanced AI)

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Notes
- Video streaming/recording uses WebRTC (frontend JS) and Django Channels (backend signaling).
- Replace `YOUR_NAME_OR_COMPANY` in LICENSE with your details.
- For production, configure media storage and security settings.
