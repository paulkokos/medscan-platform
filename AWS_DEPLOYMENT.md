# AWS Deployment Guide

Complete guide for deploying MedScan Platform to AWS.

<br>

---

## Architecture Overview

<br>

| Component     | AWS Service       | Purpose                      |
| ------------- | ----------------- | ---------------------------- |
| Backend API   | Elastic Beanstalk | Django application hosting   |
| Frontend      | S3 + CloudFront   | Static website hosting & CDN |
| Database      | RDS PostgreSQL    | Managed database service     |
| Media Storage | S3                | User-uploaded images         |
| Domain & SSL  | Route 53 + ACM    | DNS and SSL certificates     |

<br>

---

## Prerequisites

<br>

### 1. AWS Account

- Sign up at https://aws.amazon.com/free/
- Free tier includes:
  - 750 hours EC2 t2.micro per month (12 months)
  - 750 hours RDS db.t2.micro per month (12 months)
  - 5GB S3 storage
  - 1 million Lambda requests per month

<br>

### 2. Install AWS CLI

```bash
# Linux/macOS
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

<br>

### 3. Configure AWS Credentials

```bash
aws configure
```

You will need:

- AWS Access Key ID
- AWS Secret Access Key
- Default region: `us-east-1`
- Default output format: `json`

To get credentials:

1. Go to AWS Console
2. IAM > Users > Your User > Security Credentials
3. Create Access Key

<br>

### 4. Install EB CLI

```bash
pip install awsebcli --upgrade --user

# Verify installation
eb --version
```

<br>

---

## Step 1: Setup RDS PostgreSQL Database

<br>

### Option A: Using Script (Recommended)

```bash
cd aws
./setup-database.sh medscan-db medscan medscan YOUR_SECURE_PASSWORD us-east-1
```

<br>

### Option B: Manual Setup

**1. Create Database:**

```bash
aws rds create-db-instance \
    --db-instance-identifier medscan-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 16.1 \
    --master-username medscan \
    --master-user-password YOUR_SECURE_PASSWORD \
    --allocated-storage 20 \
    --publicly-accessible \
    --db-name medscan
```

**2. Wait for database to be ready:**

```bash
aws rds wait db-instance-available --db-instance-identifier medscan-db
```

**3. Get database endpoint:**

```bash
aws rds describe-db-instances \
    --db-instance-identifier medscan-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text
```

**4. Configure Security Group:**

1. Go to RDS Console
2. Select your database
3. Security > VPC security groups
4. Edit inbound rules
5. Add rule: PostgreSQL (5432) from Anywhere (0.0.0.0/0) for testing
6. For production: restrict to Elastic Beanstalk security group only

<br>

---

## Step 2: Deploy Backend to Elastic Beanstalk

<br>

### Initialize EB Application

```bash
cd backend

# Initialize Elastic Beanstalk
eb init -p python-3.11 medscan-platform --region us-east-1

# Create environment
eb create medscan-env \
    --instance-type t2.micro \
    --database.engine postgres \
    --database.instance db.t3.micro \
    --envvars SECRET_KEY=your-secret-key,DEBUG=False
```

<br>

### Set Environment Variables

```bash
# Database connection
eb setenv DATABASE_URL=postgresql://medscan:YOUR_PASSWORD@YOUR_RDS_ENDPOINT:5432/medscan

# Django settings
eb setenv SECRET_KEY=your-super-secret-key-here
eb setenv DEBUG=False
eb setenv ALLOWED_HOSTS=.elasticbeanstalk.com,.yourdomain.com

# CORS
eb setenv CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

<br>

### Deploy Application

```bash
# Using script
cd ../aws
./deploy-backend.sh

# Or manually
cd ../backend
eb deploy
```

<br>

### Verify Deployment

```bash
# Check environment status
eb status

# Check health
eb health

# View logs
eb logs

# Open application in browser
eb open
```

<br>

---

## Step 3: Deploy Frontend to S3 + CloudFront

<br>

### Deploy to S3

```bash
# Using script
cd aws
./deploy-frontend.sh medscan-frontend us-east-1

# Or manually - see below
```

<br>

### Manual S3 Deployment

**1. Build React app:**

```bash
cd frontend
npm run build
```

**2. Create S3 bucket:**

```bash
aws s3api create-bucket \
    --bucket medscan-frontend \
    --region us-east-1
```

**3. Configure for static website:**

```bash
aws s3 website s3://medscan-frontend \
    --index-document index.html \
    --error-document index.html
```

**4. Set bucket policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::medscan-frontend/*"
    }
  ]
}
```

```bash
aws s3api put-bucket-policy \
    --bucket medscan-frontend \
    --policy file://bucket-policy.json
```

**5. Upload files:**

```bash
aws s3 sync build/ s3://medscan-frontend --delete
```

<br>

### Setup CloudFront CDN

**1. Create distribution:**

```bash
aws cloudfront create-distribution \
    --origin-domain-name medscan-frontend.s3-website-us-east-1.amazonaws.com \
    --default-root-object index.html
```

**2. Or use AWS Console:**

1. Go to CloudFront Console
2. Create Distribution
3. Origin Domain: `medscan-frontend.s3-website-us-east-1.amazonaws.com`
4. Viewer Protocol Policy: Redirect HTTP to HTTPS
5. Default Root Object: `index.html`
6. Create Distribution

<br>

---

## Step 4: Configure Domain & SSL

<br>

### Register Domain (Route 53)

```bash
# Check domain availability
aws route53domains check-domain-availability --domain-name yourdomain.com

# Register domain (costs ~$12/year)
aws route53domains register-domain \
    --domain-name yourdomain.com \
    --duration-in-years 1 \
    --admin-contact file://contact.json \
    --registrant-contact file://contact.json \
    --tech-contact file://contact.json
```

<br>

### Request SSL Certificate (ACM)

```bash
# Request certificate
aws acm request-certificate \
    --domain-name yourdomain.com \
    --subject-alternative-names www.yourdomain.com api.yourdomain.com \
    --validation-method DNS \
    --region us-east-1

# Verify via email or DNS
# Follow instructions in AWS Console
```

<br>

### Configure DNS

**1. Create hosted zone:**

```bash
aws route53 create-hosted-zone \
    --name yourdomain.com \
    --caller-reference $(date +%s)
```

**2. Add records:**

- A record for `yourdomain.com` → CloudFront distribution
- A record for `www.yourdomain.com` → CloudFront distribution
- CNAME for `api.yourdomain.com` → Elastic Beanstalk URL

<br>

---

## Step 5: Configure S3 for Media Files

<br>

### Create Media Bucket

```bash
aws s3api create-bucket \
    --bucket medscan-media \
    --region us-east-1

# Set CORS policy
aws s3api put-bucket-cors \
    --bucket medscan-media \
    --cors-configuration file://cors-config.json
```

<br>

### Update Django Settings

Add to `backend/medscan/settings.py`:

```python
# S3 Storage Configuration
if os.environ.get('USE_S3') == 'True':
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Media files
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
```

<br>

### Set Environment Variables

```bash
eb setenv USE_S3=True
eb setenv AWS_STORAGE_BUCKET_NAME=medscan-media
eb setenv AWS_S3_REGION_NAME=us-east-1
```

<br>

---

## Cost Estimation

<br>

### Free Tier (First 12 Months)

| Service         | Free Tier        | After Free Tier   |
| --------------- | ---------------- | ----------------- |
| EC2 t2.micro    | 750 hours/month  | $8.50/month       |
| RDS db.t2.micro | 750 hours/month  | $15/month         |
| S3 Storage      | 5GB              | $0.023/GB         |
| CloudFront      | 50GB transfer    | $0.085/GB         |
| Route 53        | $0.50/month      | $0.50/month       |
| **Total**       | **~$0.50/month** | **~$25-30/month** |

<br>

---

## Monitoring & Maintenance

<br>

### View Logs

```bash
# Backend logs
eb logs

# CloudWatch logs
aws logs tail /aws/elasticbeanstalk/medscan-env/var/log/eb-engine.log --follow
```

<br>

### Monitor Costs

```bash
# Current month costs
aws ce get-cost-and-usage \
    --time-period Start=$(date -d "1 month ago" +%Y-%m-01),End=$(date +%Y-%m-%d) \
    --granularity MONTHLY \
    --metrics UnblendedCost
```

<br>

### Set Billing Alerts

1. Go to CloudWatch Console
2. Billing > Create Alarm
3. Set threshold (e.g., $10)
4. Add email notification

<br>

---

## Cleanup Resources

<br>

To avoid charges, delete all resources:

```bash
cd aws
./cleanup.sh
```

Or manually:

```bash
# Terminate EB environment
eb terminate --all

# Delete RDS database
aws rds delete-db-instance \
    --db-instance-identifier medscan-db \
    --skip-final-snapshot

# Empty and delete S3 buckets
aws s3 rm s3://medscan-frontend --recursive
aws s3 rb s3://medscan-frontend

aws s3 rm s3://medscan-media --recursive
aws s3 rb s3://medscan-media

# Delete CloudFront distribution (must disable first)
# Delete Route 53 hosted zone
# Delete ACM certificate
```

<br>

---

## Troubleshooting

<br>

### Common Issues

**1. Database connection refused:**

- Check RDS security group allows inbound from EB security group
- Verify DATABASE_URL is correct
- Check RDS instance is running

**2. Static files not loading:**

- Run `eb deploy` after collecting static files
- Check S3 bucket policy allows public read
- Verify CloudFront distribution is deployed

**3. 502 Bad Gateway:**

- Check EB logs: `eb logs`
- Verify WSGI path in `.ebextensions/02_python.config`
- Check application is running: `eb ssh` then `sudo systemctl status web`

**4. Migration errors:**

- SSH into instance: `eb ssh`
- Run migrations manually: `cd /var/app/current && source /var/app/venv/*/bin/activate && python manage.py migrate`

<br>

---

## Next Steps

1. Set up continuous deployment from GitHub
2. Configure monitoring with CloudWatch
3. Set up backup automation for RDS
4. Implement auto-scaling policies
5. Add Redis for caching (ElastiCache)
6. Set up staging environment

<br>

---

## Useful Commands Cheat Sheet

```bash
# Elastic Beanstalk
eb init                 # Initialize EB application
eb create               # Create new environment
eb deploy               # Deploy application
eb status               # Check environment status
eb health               # Check health
eb logs                 # View logs
eb open                 # Open in browser
eb ssh                  # SSH into instance
eb terminate            # Delete environment

# RDS
aws rds describe-db-instances              # List databases
aws rds modify-db-instance                 # Modify settings
aws rds create-db-snapshot                 # Create backup

# S3
aws s3 ls                                  # List buckets
aws s3 sync <dir> s3://<bucket>           # Upload files
aws s3 rm s3://<bucket> --recursive       # Delete files

# CloudFront
aws cloudfront list-distributions          # List distributions
aws cloudfront create-invalidation         # Clear cache
```

<br>

---

## Support

For issues with AWS deployment:

- AWS Documentation: https://docs.aws.amazon.com/
- Elastic Beanstalk Guide: https://docs.aws.amazon.com/elasticbeanstalk/
- AWS Support: https://console.aws.amazon.com/support/

<br>

---

Last Updated: 2025-01-15
