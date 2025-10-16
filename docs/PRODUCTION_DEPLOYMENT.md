# MedScan Platform - Production Deployment Guide

This document provides comprehensive instructions for deploying MedScan Platform to a production environment.

## Table of Contents

1. [Pre-deployment Checklist](#pre-deployment-checklist)
2. [Prerequisites](#prerequisites)
3. [Environment Configuration](#environment-configuration)
4. [Docker Deployment](#docker-deployment)
5. [SSL/TLS Configuration](#ssltls-configuration)
6. [Security Hardening](#security-hardening)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup & Recovery](#backup--recovery)
9. [Troubleshooting](#troubleshooting)

---

## Pre-deployment Checklist

Before deploying to production, ensure:

- [ ] All environment variables configured in `.env.prod`
- [ ] SSL/TLS certificates obtained (Let's Encrypt recommended)
- [ ] Database backups configured
- [ ] Monitoring and alerting set up
- [ ] Security scanning completed (OWASP, Dependabot)
- [ ] Load testing performed
- [ ] Disaster recovery plan documented
- [ ] Team trained on deployment procedures
- [ ] Change log reviewed and updated
- [ ] Staged deployment tested (staging → production)

---

## Prerequisites

### System Requirements

- **OS:** Ubuntu 20.04 LTS or later / Amazon Linux 2 / RHEL 8+
- **Docker:** 20.10+ ([Install Docker](https://docs.docker.com/install/))
- **Docker Compose:** 2.0+ ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **CPU:** Minimum 2 cores (4+ recommended)
- **RAM:** Minimum 4GB (8+ recommended)
- **Storage:** 50GB+ (depends on usage)

### Domain & SSL

- Domain name pointing to your server
- SSL/TLS certificate (free via Let's Encrypt)
- DNS records configured

### Optional but Recommended

- AWS account (for S3 storage, CloudWatch)
- Sentry account (error tracking)
- SendGrid/Mailgun account (email service)

---

## Environment Configuration

### 1. Prepare Environment Files

```bash
# Copy production environment template
cp backend/.env.prod.example backend/.env.prod

# Edit with your production values
nano backend/.env.prod
```

**Critical settings to configure:**

```env
SECRET_KEY=your-secret-key           # Generate random key
DB_PASSWORD=strong-password          # Use strong credentials
ALLOWED_HOSTS=yourdomain.com         # Your domain
CORS_ALLOWED_ORIGINS=https://yourdomain.com
JWT_SECRET_KEY=your-jwt-secret
```

### 2. Create SSL Directory Structure

```bash
mkdir -p nginx/ssl
# Place your SSL certificate files here
# cert.pem - Your SSL certificate
# key.pem - Your private key
```

### 3. Create Nginx Directories

```bash
mkdir -p nginx/logs
chmod 755 nginx/logs
```

---

## Docker Deployment

### 1. Pull/Update Images

```bash
docker-compose -f docker-compose.prod.yml pull
```

### 2. Build Images

```bash
docker-compose -f docker-compose.prod.yml build --no-cache
```

### 3. Start Services

```bash
# Start in background
docker-compose -f docker-compose.prod.yml up -d

# Verify services are running
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### 4. Run Database Migrations

```bash
# Execute inside running backend container
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# Create superuser (optional)
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 5. Collect Static Files

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

---

## SSL/TLS Configuration

### Option 1: Let's Encrypt (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Copy certificates to nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
sudo chown $USER:$USER nginx/ssl/*
sudo chmod 400 nginx/ssl/key.pem

# Auto-renew (add to crontab)
0 3 * * * /usr/bin/certbot renew --quiet && docker-compose -f docker-compose.prod.yml restart nginx
```

### Option 2: AWS Certificate Manager

If using AWS, leverage ACM with ALB/NLB instead.

---

## Security Hardening

### 1. Update Docker Compose

Ensure `docker-compose.prod.yml` includes:

```yaml
# Database - No external ports
postgres:
  ports: []  # Not exposed to internet

# Backend - Only internal networking
backend:
  ports: []  # Not exposed to internet

# Nginx - Only exposed service
nginx:
  ports:
    - "80:80"
    - "443:443"
```

### 2. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### 3. Environment Validation

Ensure `.env.prod` has no insecure defaults:

```bash
# Verify SECRET_KEY is not default
grep "django-insecure" backend/.env.prod
# Should return nothing

# Verify DEBUG is False
grep "DEBUG" backend/.env.prod
# Should show: DEBUG=False
```

### 4. Docker Security

```bash
# Run as non-root (configured in Dockerfile)
docker-compose -f docker-compose.prod.yml exec backend id
# Should NOT be root

# Use read-only filesystem where possible
# Use resource limits (configured in docker-compose.prod.yml)
```

### 5. Database Security

```bash
# Set strong password in .env.prod
DB_PASSWORD=generate-strong-password-here

# Enable database connection encryption
# Backup database regularly
```

---

## Monitoring & Logging

### 1. View Logs

```bash
# All services
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f backend

# Nginx logs
docker-compose -f docker-compose.prod.yml logs -f nginx
```

### 2. Monitor Container Health

```bash
# Check container status
docker-compose -f docker-compose.prod.yml ps

# View resource usage
docker stats

# Check service health
curl http://localhost/health
```

### 3. Set Up Monitoring (Optional)

- **Prometheus:** Container metrics
- **Grafana:** Visualization dashboard
- **Sentry:** Application error tracking
- **DataDog/New Relic:** Full observability

### 4. Log Rotation

```bash
# Configure Docker log rotation
cat /etc/docker/daemon.json
# Add:
# {
#   "log-driver": "json-file",
#   "log-opts": {
#     "max-size": "10m",
#     "max-file": "3"
#   }
# }
```

---

## Backup & Recovery

### 1. Database Backups

```bash
# Manual backup
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U medscan_user medscan_prod > backup.sql

# Restore from backup
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U medscan_user medscan_prod < backup.sql

# Automated daily backup (add to crontab)
0 2 * * * docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U $DB_USER $DB_NAME > /backups/medscan-$(date +\%Y\%m\%d).sql
```

### 2. Media Files Backup

```bash
# If using local storage
tar -czf media-backup-$(date +%Y%m%d).tar.gz backend/media/

# If using S3, enable versioning in bucket
```

### 3. Disaster Recovery Procedure

```bash
# 1. Stop services
docker-compose -f docker-compose.prod.yml down

# 2. Restore database
docker-compose -f docker-compose.prod.yml up -d postgres
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U medscan_user < backup.sql

# 3. Restore media files
tar -xzf media-backup-YYYYMMDD.tar.gz

# 4. Start all services
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml logs backend

# Common issues:
# 1. Port already in use: sudo lsof -i :PORT
# 2. Volume permission denied: sudo chown -R $USER:$USER volumes
# 3. Environment variable missing: grep "variable-name" .env.prod
```

### Database Connection Failing

```bash
# Test database connection
docker-compose -f docker-compose.prod.yml exec backend python manage.py dbshell

# Check DATABASE_URL format
# Should be: postgresql://user:password@postgres:5432/dbname
```

### Migrations Failing

```bash
# Rollback to previous migration
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate app_name 0001

# Then reapply
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

### Nginx 502 Bad Gateway

```bash
# Usually means backend is down
docker-compose -f docker-compose.prod.yml ps backend

# Restart backend
docker-compose -f docker-compose.prod.yml restart backend

# Check backend logs
docker-compose -f docker-compose.prod.yml logs backend
```

### Certificate Renewal Issues

```bash
# Manually renew Let's Encrypt certificate
sudo certbot renew --dry-run

# Copy renewed certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem

# Restart Nginx
docker-compose -f docker-compose.prod.yml restart nginx
```

---

## Performance Tuning

### 1. Database Connection Pooling

In `backend/.env.prod`:
```env
DATABASE_CONN_MAX_AGE=600
DATABASE_CONN_HEALTH_CHECKS=True
```

### 2. Gunicorn Workers

```env
GUNICORN_WORKERS=4  # CPU_CORES * 2 + 1
```

### 3. Nginx Caching

Already configured in `nginx/nginx.prod.conf`:
- Static files: 30 days cache
- Media files: 7 days cache
- Gzip compression enabled

### 4. Database Optimization

```bash
# Analyze slow queries
EXPLAIN ANALYZE SELECT ... ;

# Create indexes on frequently queried columns
```

---

## Maintenance

### Regular Tasks

- **Daily:** Check logs, verify backups
- **Weekly:** Review security updates, update dependencies
- **Monthly:** Performance review, certificate expiration check
- **Quarterly:** Security audit, disaster recovery test
- **Yearly:** Full system review, capacity planning

### Update Procedures

```bash
# 1. Backup everything
# 2. Pull latest images
docker-compose -f docker-compose.prod.yml pull

# 3. Rebuild containers
docker-compose -f docker-compose.prod.yml build

# 4. Test in staging first
# 5. Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# 6. Verify services
docker-compose -f docker-compose.prod.yml ps
```

---

## Support & Documentation

- **API Docs:** `https://yourdomain.com/api/docs/`
- **Admin Panel:** `https://yourdomain.com/admin/`
- **GitHub Issues:** [MedScan Platform Issues](https://github.com/paulkokos/medscan-platform/issues)

---

Last Updated: 2025-10-17
Version: 1.0.0
