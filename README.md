# Engineer Konnect

A full-stack web application connecting engineers worldwide. Built with Django, SQLite, and HTML/CSS.

## Features

- **User Authentication** - Register, login, and manage profiles
- **Job Board** - Browse and apply for engineering jobs
- **Discussions** - Engage in community discussions
- **Messaging** - Direct messaging between users
- **Engineer Profiles** - Showcase your skills and experience
- **RESTful API** - Complete REST API for integration

## Tech Stack

- **Backend**: Django 4.1.13, Django REST Framework
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: Token-based authentication
- **Other**: CORS support, Pillow for image handling

## Installation

### Prerequisites
- Python 3.10+
- pip
- git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/engineer-konnect.git
   cd engineer-konnect
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   MONGO_URI=mongodb://localhost:27017
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit in browser**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/

## API Endpoints

- `POST /api/auth/login/` - Login and get token
- `POST /api/users/register/` - Register new user
- `GET /api/users/profiles/` - List user profiles
- `GET /api/discussions/` - List discussions
- `GET /api/jobs/` - List job postings
- `GET /api/messages/` - List conversations

## Project Structure

```
engineer-konnect/
├── engineer_connect/     # Main Django project
├── users/                # User app
├── discussions/          # Discussions app
├── jobs/                 # Jobs app
├── messaging/            # Messaging app
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── manage.py
├── requirements.txt
└── README.md
```

## Usage

### Register a New User
1. Visit http://127.0.0.1:8000/register/
2. Fill in the registration form
3. Click "Register"

### Login
1. Visit http://127.0.0.1:8000/login/
2. Enter your credentials
3. You'll be redirected to dashboard

### Browse Jobs
1. Go to http://127.0.0.1:8000/jobs/
2. Search or browse available jobs
3. Click "Apply Now" to apply

### Join Discussions
1. Go to http://127.0.0.1:8000/discussions/
2. View community discussions
3. Click on a discussion to see details

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Developer

Developed by **Kleins Dickson** from **General Electric**

## Support

For support, email support@engineerkonnect.com or open an issue on GitHub.

---

© 2026 Engineer Konnect. Connecting engineers worldwide.
