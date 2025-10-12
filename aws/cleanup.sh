#!/bin/bash

set -e

echo "=========================================="
echo "AWS Resources Cleanup Script"
echo "=========================================="
echo "WARNING: This will delete all AWS resources"
echo "=========================================="
echo ""

read -p "Are you sure you want to continue? (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Cleanup cancelled"
    exit 0
fi

echo "Terminating Elastic Beanstalk environment..."
cd "$(dirname "$0")/../backend"
eb terminate --all --force || echo "EB environment not found or already terminated"

echo "Deleting RDS database..."
aws rds delete-db-instance \
    --db-instance-identifier medscan-db \
    --skip-final-snapshot \
    --delete-automated-backups || echo "RDS instance not found"

echo "Emptying S3 bucket..."
aws s3 rm s3://medscan-frontend --recursive || echo "S3 bucket not found"

echo "Deleting S3 bucket..."
aws s3api delete-bucket \
    --bucket medscan-frontend || echo "S3 bucket not found"

echo "Deleting CloudWatch logs..."
aws logs delete-log-group \
    --log-group-name /aws/elasticbeanstalk/medscan-env/var/log/eb-engine.log || echo "Log group not found"

echo "=========================================="
echo "Cleanup completed!"
echo "=========================================="
echo ""
echo "Note: Some resources may take a few minutes to fully delete"
