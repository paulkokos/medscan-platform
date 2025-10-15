# MedScan Platform

> AI-Powered Medical Image Segmentation Platform

<br>

[![Frontend CI](https://github.com/paulkokos/medscan-platform/workflows/Frontend%20CI/badge.svg?branch=master)](https://github.com/paulkokos/medscan-platform/actions)
[![Backend CI](https://github.com/paulkokos/medscan-platform/workflows/Backend%20CI/badge.svg?branch=master)](https://github.com/paulkokos/medscan-platform/actions)
[![codecov](https://codecov.io/gh/paulkokos/medscan-platform/branch/master/graph/badge.svg)](https://github.com/paulkokos/medscan-platform/actions)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Discussions](https://img.shields.io/github/discussions/paulkokos/medscan-platform)](https://github.com/paulkokos/medscan-platform/discussions)
[![Project Board](https://img.shields.io/badge/project-board-blue)](https://github.com/users/paulkokos/projects)
[![Issues](https://img.shields.io/github/issues/paulkokos/medscan-platform)](https://github.com/paulkokos/medscan-platform/issues)

<br>
<br>

---

## Overview

MedScan Platform is a full-stack web application designed for medical image analysis and segmentation using deep learning. The platform enables healthcare professionals and researchers to upload medical images (CT scans, MRI, X-rays) and receive automated segmentation results powered by TensorFlow/Keras neural networks.

<br>

### Key Features

<br>

| Feature | Description |
|---------|-------------|
| **AI-Powered Analysis** | Advanced deep learning models for medical image segmentation |
| **User Authentication** | Secure JWT-based authentication system |
| **Image Management** | Upload, view, and manage medical images |
| **Real-time Processing** | Asynchronous image analysis with progress tracking |
| **Interactive Dashboard** | Visualize segmentation results with Chart.js |
| **RESTful API** | Well-documented API for integration |
| **Responsive Design** | Mobile-friendly interface with Tailwind CSS |
| **Docker Support** | Containerized deployment for easy setup |
| **CI/CD Pipeline** | Automated testing and deployment with GitHub Actions |

<br>
<br>

---

## Tech Stack

<br>

### Frontend

![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Redux](https://img.shields.io/badge/redux-%23593d88.svg?style=for-the-badge&logo=redux&logoColor=white)
![React Router](https://img.shields.io/badge/React_Router-CA4245?style=for-the-badge&logo=react-router&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)

- React 18 with Hooks
- Redux Toolkit for state management
- React Router v6 for client-side routing
- Tailwind CSS for styling
- Axios for HTTP requests
- Chart.js for data visualization

<br>

### Backend

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)

- Django 5.0 - High-level Python web framework
- Django REST Framework - API toolkit
- PostgreSQL - Relational database
- TensorFlow/Keras - Deep learning framework
- JWT Authentication - Secure token-based auth
- Pillow - Image processing

<br>

### DevOps

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

- Docker & Docker Compose - Containerization
- GitHub Actions - CI/CD pipelines
- Nginx - Reverse proxy and static file serving

<br>
<br>

---

## Quick Start

<br>

### Prerequisites

```
Node.js 18+
Python 3.11+
PostgreSQL 16+
Docker & Docker Compose (optional)
```

<br>

### Installation

<br>

#### Option 1: Docker (Recommended)

**1. Clone the repository**
```bash
git clone https://github.com/paulkokos/medscan-platform.git
cd medscan-platform
```

**2. Create environment file**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your configuration
```

**3. Start services**
```bash
docker-compose up -d
```

**4. Access the application**

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

<br>
<br>

#### Option 2: Manual Setup

**Backend Setup:**

```bash
cd backend

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

**Frontend Setup:**

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

<br>

**Access the application:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

<br>
<br>

---

## Project Structure

```
medscan-platform/
├── .github/
│   ├── workflows/           # CI/CD workflows
│   └── ISSUE_TEMPLATE/      # Issue templates
├── frontend/                # React application
│   ├── public/
│   └── src/
│       ├── components/      # React components
│       ├── pages/           # Page components
│       ├── redux/           # State management
│       └── services/        # API services
├── backend/                 # Django application
│   ├── apps/
│   │   ├── authentication/  # User authentication
│   │   ├── images/          # Image management
│   │   └── analysis/        # ML analysis
│   └── medscan/             # Project settings
└── docker-compose.yml       # Docker orchestration
```

<br>
<br>

---

## API Documentation

<br>

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login and get JWT token |
| GET | `/api/auth/user/` | Get current user profile |

<br>

### Images Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/images/` | List all images |
| POST | `/api/images/` | Upload new image |
| GET | `/api/images/{id}/` | Get image details |
| DELETE | `/api/images/{id}/` | Delete image |

<br>

### Analysis Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analysis/` | Start analysis |
| GET | `/api/analysis/{id}/` | Get analysis results |

<br>

For detailed API documentation, visit `/api/docs/` when running the server.

<br>
<br>

---

## Development

<br>

### Running Tests

**Frontend:**
```bash
cd frontend
npm test              # Run tests
npm run test:coverage # Run with coverage
npm run lint          # Run ESLint
npm run format        # Format with Prettier
```

<br>

**Backend:**
```bash
cd backend
pytest                  # Run tests
pytest --cov            # Run with coverage
black .                 # Format code
pylint **/*.py          # Lint code
```

<br>

### Code Style

- **Frontend**: ESLint + Prettier (Airbnb style guide)
- **Backend**: Black + isort + Pylint (PEP 8)

<br>

### Git Workflow

We follow the [GitHub Flow](https://guides.github.com/introduction/flow/):

1. Create a feature branch from `main`
2. Make changes and commit
3. Push and create a pull request
4. Code review and CI checks
5. Merge to `main`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

<br>
<br>

---

## Deployment

<br>

### Production Deployment

1. Update environment variables for production
2. Build Docker images
3. Deploy using docker-compose or orchestration tool

```bash
docker-compose -f docker-compose.prod.yml up -d
```

<br>

### Environment Variables

See `backend/.env.example` for required environment variables.

<br>
<br>

---

## Security

For security vulnerabilities, please see [SECURITY.md](SECURITY.md).

**Security Features:**
- Secret Scanning with Push Protection
- Dependabot Security Updates
- Branch Protection Rules
- CodeQL Analysis (JavaScript + Python)
- SAST Scanning with Semgrep

<br>
<br>

---

## Contributing

### [Join the Discussion](https://github.com/paulkokos/medscan-platform/discussions)
- Ask questions and get help from the community
- Share ideas for new features and improvements
- Showcase your implementations and use cases
- Discuss medical imaging research and techniques
- Collaborate on development and best practices

### [Project Board](https://github.com/users/paulkokos/projects)
- View current development priorities and roadmap
- See what features are planned and in progress
- Contribute to ongoing tasks and initiatives
- Track bug fixes and feature requests

### How to Contribute

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

**Quick Steps:**

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<br>
<br>

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<br>

---

## Authors

**Paul Kokos** - [paulkokos](https://github.com/paulkokos)

<br>

---

## Acknowledgments

- TensorFlow team for the deep learning framework
- Django REST Framework for the excellent API toolkit
- React team for the amazing UI library
- All contributors who help improve this project

<br>
<br>

---

## Project Status

**Current Version:** 0.1.0 (Alpha)

This project is under active development. Features and API may change.

<br>

### Roadmap

- [ ] Implement U-Net architecture for segmentation
- [ ] Add support for DICOM file format
- [ ] Real-time collaboration features
- [ ] Export results to PDF reports
- [ ] Integration with PACS systems
- [ ] Multi-language support
- [ ] Mobile application

<br>
<br>

---

## Contact

**Project Link:** [https://github.com/paulkokos/medscan-platform](https://github.com/paulkokos/medscan-platform)

<br>

---

<div align="center">

Made with care for the medical imaging community

</div>












