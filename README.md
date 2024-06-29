```markdown
# Eventasya Django Backend

Eventasya is a mobile application for managing events, renting venues, and an exhibition of the previous work of event organizers and planners.
The backend is powered by Django Rest Framework and utilizes MySQL for the database. Firebase is integrated for real-time chat functionality and user authentication.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Firebase Setup](#firebase-setup)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features
- User registration and authentication with Django.
- Event creation and management.
- Event booking with unique booking IDs.
- Real-time chat integration using Firebase.
- Image uploads for events.

## Technologies Used
- Django Rest Framework
- MySQL (Database)
- Railway (MySQL Database Hosting)
- Render (Deployment)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/eventasya.git
   cd eventasya
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database in `settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_database_user',
           'PASSWORD': 'your_database_password',
           'HOST': 'your_database_host',
           'PORT': 'your_database_port',
       }
   }
   ```

5. Initialize Firebase in your Django project:
   ```python
   import firebase_admin
   from firebase_admin import credentials

   cred = credentials.Certificate("path/to/your/firebase/credentials.json")
   firebase_admin.initialize_app(cred)
   ```

6. Apply the migrations:
   ```bash
   python manage.py migrate
   ```

7. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
- Access the Django admin panel at `http://localhost:8000/admin` to manage users and events.

## API Endpoints
### Authentication
- `POST /accounts/signup/` - Register a new user.
- `POST /accounts/login/` - Login a user and generate Firebase token.

### Events
- `GET /events/` - List all events.
- `POST /events/` - Create a new event.
- `GET /events/{id}/` - Get event details.
- `POST /events/{id}/book/` - Book an event.

### Chat
- Real-time chat is implemented using Firebase. The backend handles the generation and validation of Firebase tokens for authenticated users.

## Firebase Setup
1. Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
2. Navigate to "Project Settings" and add a new service account.
3. Generate a private key and download the `credentials.json` file.
4. Place the `credentials.json` file in your Django project directory and reference it in your settings or initialization code as shown above.

## Project Structure
```
eventasya/
├── accounts/
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── events/
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── chat/
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── manage.py
└── ...
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
```
