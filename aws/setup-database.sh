#!/bin/bash

set -e

echo "=========================================="
echo "AWS RDS PostgreSQL Setup Script"
echo "=========================================="

DB_INSTANCE_ID=${1:-"medscan-db"}
DB_NAME=${2:-"medscan"}
DB_USERNAME=${3:-"medscan"}
DB_PASSWORD=${4}
REGION=${5:-"us-east-1"}

if [ -z "$DB_PASSWORD" ]; then
    echo "Error: Database password is required"
    echo "Usage: $0 [instance-id] [db-name] [username] <password> [region]"
    exit 1
fi

echo "Checking AWS credentials..."
aws sts get-caller-identity > /dev/null 2>&1 || {
    echo "Error: AWS credentials not configured"
    echo "Please run 'aws configure'"
    exit 1
}

echo "Creating RDS PostgreSQL instance..."
aws rds create-db-instance \
    --db-instance-identifier "$DB_INSTANCE_ID" \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --engine-version 16.1 \
    --master-username "$DB_USERNAME" \
    --master-user-password "$DB_PASSWORD" \
    --allocated-storage 20 \
    --storage-type gp2 \
    --publicly-accessible \
    --backup-retention-period 7 \
    --preferred-backup-window "03:00-04:00" \
    --preferred-maintenance-window "mon:04:00-mon:05:00" \
    --db-name "$DB_NAME" \
    --region "$REGION" \
    --tags Key=Name,Value=medscan-database Key=Environment,Value=production

echo "Waiting for database to be available (this may take 5-10 minutes)..."
aws rds wait db-instance-available \
    --db-instance-identifier "$DB_INSTANCE_ID" \
    --region "$REGION"

echo "Getting database endpoint..."
DB_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier "$DB_INSTANCE_ID" \
    --region "$REGION" \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text)

echo "=========================================="
echo "Database created successfully!"
echo "=========================================="
echo ""
echo "Database Endpoint: $DB_ENDPOINT"
echo "Database Name: $DB_NAME"
echo "Username: $DB_USERNAME"
echo ""
echo "Add this to your Elastic Beanstalk environment variables:"
echo "DATABASE_URL=postgresql://$DB_USERNAME:$DB_PASSWORD@$DB_ENDPOINT:5432/$DB_NAME"
echo ""
echo "To set environment variable:"
echo "eb setenv DATABASE_URL=postgresql://$DB_USERNAME:$DB_PASSWORD@$DB_ENDPOINT:5432/$DB_NAME"
