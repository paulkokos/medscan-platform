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

