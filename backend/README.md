# MedScan Platform - Backend

Django REST API for MedScan medical image analysis platform.

<br>

---

## Tech Stack

<br>

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 5.0 | Web framework |
| **Django REST Framework** | 3.14+ | API toolkit |
| **PostgreSQL** | 16+ | Database |
| **JWT** | - | Authentication |
| **TensorFlow/Keras** | 2.19+ | ML inference |
| **Gunicorn** | - | WSGI server |
| **WhiteNoise** | - | Static files |

<br>

---

## Setup

<br>

### Prerequisites

- Python 3.11+
- PostgreSQL 16+
- Virtual environment

<br>

### Installation

**1. Clone and navigate to backend:**
```bash
cd backend
```

<br>

**2. Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

<br>

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

<br>

**4. Setup database:**
```bash
# Create PostgreSQL database
createdb medscan

# Configure environment
cp .env.example .env
# Edit .env with your database credentials and secrets
```

<br>

**5. Run migrations:**
```bash
python manage.py migrate
```

<br>

**6. Create superuser:**
```bash
python manage.py createsuperuser
```

<br>

**7. Start development server:**
```bash
python manage.py runserver
```

The API will be available at [http://localhost:8000](http://localhost:8000)

<br>

---

## API Endpoints

<br>

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get JWT token |
| POST | `/api/auth/token/refresh/` | Refresh JWT token |
| GET | `/api/auth/user/` | Get current user profile |
| PATCH | `/api/auth/user/` | Update user profile |
| DELETE | `/api/auth/user/` | Delete user account |

<br>

### Images

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/images/` | List all user's images |
| POST | `/api/images/` | Upload new image |
| GET | `/api/images/{id}/` | Get image details |
| PATCH | `/api/images/{id}/` | Update image metadata |
| DELETE | `/api/images/{id}/` | Delete image |

<br>

### Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analysis/` | Start image analysis |
| GET | `/api/analysis/` | List all analyses |
| GET | `/api/analysis/{id}/` | Get analysis results |
| DELETE | `/api/analysis/{id}/` | Delete analysis |

<br>

---

## Testing

<br>

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test module
pytest apps/authentication/tests/

# Run specific test file
pytest apps/authentication/tests/test_views.py

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s
```

<br>

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

<br>

---

## Code Quality

<br>

### Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Run both
black . && isort .
```

<br>

### Linting

```bash
# Check with flake8
flake8 .

# Check with pylint
pylint apps/
```

<br>

### Type Checking

```bash
# Run mypy (if configured)
mypy apps/
```

<br>

---

## Project Structure

<br>

```
backend/
├── apps/
│   ├── authentication/       # User authentication & JWT
│   │   ├── models.py        # Custom User model
│   │   ├── serializers.py   # Auth serializers
│   │   ├── views.py         # Auth endpoints
│   │   ├── urls.py          # Auth routes
│   │   └── tests/           # Unit & integration tests
│   ├── images/              # Medical image management
│   │   ├── models.py        # MedicalImage model
│   │   ├── serializers.py   # Image serializers
│   │   ├── views.py         # Image CRUD endpoints
│   │   ├── urls.py          # Image routes
│   │   └── tests/           # Image tests
│   └── analysis/            # ML analysis
│       ├── models.py        # Analysis model
│       ├── serializers.py   # Analysis serializers (TODO)
│       ├── views.py         # Analysis endpoints (TODO)
│       ├── urls.py          # Analysis routes
│       └── ml_service.py    # ML inference (TODO)
├── medscan/                 # Project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── media/                   # User-uploaded files
├── staticfiles/             # Collected static files
├── logs/                    # Application logs
├── tests/                   # Project-level tests
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── .env.example           # Environment variables template
└── pytest.ini             # Pytest configuration
```

<br>

---

## Environment Variables

<br>

Create a `.env` file based on `.env.example`:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://medscan:medscan@localhost:5432/medscan

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# API Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_API_REQUESTS_PER_MINUTE=60
RATE_LIMIT_USER_REQUESTS_PER_MINUTE=120
RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE=5

# Media and Static Files
MEDIA_ROOT=/app/media
STATIC_ROOT=/app/staticfiles

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# TensorFlow/ML Settings
TF_ENABLE_ONEDNN_OPTS=0
TF_CPP_MIN_LOG_LEVEL=2

# AWS S3 (optional, for production)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=us-east-1
```

<br>

---

## Admin Panel

<br>

Access the Django admin interface:
- URL: [http://localhost:8000/admin](http://localhost:8000/admin)
- Login with superuser credentials created during setup

<br>

**Features:**
- User management
- Image management
- Analysis results viewing
- Database administration

<br>

---

## API Documentation

<br>

Interactive API documentation is auto-generated using **drf-spectacular**:

| Tool | URL | Description |
|------|-----|-------------|
| **Swagger UI** | [/api/docs/](http://localhost:8000/api/docs/) | Interactive API explorer |
| **ReDoc** | [/api/redoc/](http://localhost:8000/api/redoc/) | Clean API documentation |
| **OpenAPI Schema** | [/api/schema/](http://localhost:8000/api/schema/) | Raw OpenAPI JSON |

<br>

---

## Database Management

<br>

### Migrations

```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate <app_name> <migration_name>
```

<br>

### Database Shell

```bash
# Open Django shell
python manage.py shell

# Open database shell
python manage.py dbshell
```

<br>

---

## Deployment

<br>

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup PostgreSQL database
- [ ] Configure S3 for media files
- [ ] Setup HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Enable security headers
- [ ] Setup logging and monitoring
- [ ] Run `collectstatic`
- [ ] Configure Gunicorn/uWSGI
- [ ] Setup reverse proxy (Nginx)

<br>

### Docker Deployment

```bash
# Build image
docker build -t medscan-backend .

# Run container
docker run -p 8000:8000 --env-file .env medscan-backend
```

<br>

---

## Troubleshooting

<br>

### Common Issues

**1. Database connection error:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check DATABASE_URL in .env
# Verify credentials and database exists
```

<br>

**2. Migration conflicts:**
```bash
# Reset migrations (development only)
python manage.py migrate <app> zero
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate
```

<br>

**3. Static files not loading:**
```bash
# Collect static files
python manage.py collectstatic --noinput
```

<br>

**4. Permission errors on media files:**
```bash
# Check media directory permissions
chmod -R 755 media/
```

<br>

---

## Development Tips

<br>

### Django Shell

```python
# Open Django shell
python manage.py shell

# Import models
from apps.authentication.models import User
from apps.images.models import MedicalImage

# Query examples
User.objects.all()
MedicalImage.objects.filter(user__email='test@example.com')
```

<br>

### Create Test Data

```bash
# Use Django fixtures
python manage.py loaddata fixtures/test_data.json

# Or create management command
python manage.py create_test_data
```

<br>

---

## Contributing

<br>

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation
4. Use type hints where appropriate
5. Add docstrings to functions/classes
6. Run linters before committing

<br>

---

## Authentication Hardening

<br>

- DRF throttling is enabled by default for anonymous and authenticated API traffic.
- Login, registration, token refresh, password change, and logout share a stricter auth throttle.
- Tune the rate limits with `RATE_LIMIT_API_REQUESTS_PER_MINUTE`, `RATE_LIMIT_USER_REQUESTS_PER_MINUTE`, and `RATE_LIMIT_AUTH_REQUESTS_PER_MINUTE`.

<br>

---

## Resources

<br>

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [TensorFlow Documentation](https://www.tensorflow.org/)

<br>
