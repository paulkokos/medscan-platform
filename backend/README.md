# MedScan Platform - Backend
Django REST API for MedScan medical image analysis platform.

<br>
## Tech Stack
<br>

- Django 5.0
- Django REST Framework
- PostgreSQL
- JWT Authentication
- TensorFlow/Keras

<br>

## Setup

<br>

### Prerequisites
<br>

- Python 3.11+
- PostgreSQL 16+
- Virtual environment

<br>

### Installation
<br>

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
createdb medscan
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

<br>

The API will be available at [http://localhost:8000](http://localhost:8000)

<br>

## API Endpoints

<br>

### Authentication

| Method | Endpoint              | Description              |
| ------ | --------------------- | ------------------------ |
| POST   | `/api/auth/register/` | Register new user        |
| POST   | `/api/auth/login/`    | Login and get JWT token  |
| GET    | `/api/auth/user/`     | Get current user profile |
| PATCH  | `/api/auth/user/`     | Update user profile      |

<br>

### Images

| Method | Endpoint            | Description            |
| ------ | ------------------- | ---------------------- |
| GET    | `/api/images/`      | List all user's images |
| POST   | `/api/images/`      | Upload new image       |
| GET    | `/api/images/{id}/` | Get image details      |
| DELETE | `/api/images/{id}/` | Delete image           |

<br>

### Analysis

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| POST   | `/api/analysis/`      | Start image analysis |
| GET    | `/api/analysis/{id}/` | Get analysis results |

<br>

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest apps/authentication/tests/test_views.py
```

<br>

<br>

## Code Quality

```bash
# Format code
black .
isort .

# Lint code
flake8 .
pylint **/*.py
```

<br>

<br>

