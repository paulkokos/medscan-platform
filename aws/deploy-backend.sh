#!/bin/bash

set -e

echo "=========================================="
echo "AWS Elastic Beanstalk Deployment Script"
echo "=========================================="

cd "$(dirname "$0")/../backend"

if [ ! -d ".elasticbeanstalk" ]; then
    echo "Error: .elasticbeanstalk directory not found"
    echo "Please run 'eb init' first"
    exit 1
fi

echo "Checking AWS credentials..."
aws sts get-caller-identity > /dev/null 2>&1 || {
    echo "Error: AWS credentials not configured"
    echo "Please run 'aws configure'"
    exit 1
}

echo "Creating deployment package..."
zip -r ../deploy.zip . -x "*.git*" "venv/*" "*.pyc" "__pycache__/*" "*.sqlite3" "media/*" "logs/*"

echo "Deploying to Elastic Beanstalk..."
eb deploy

echo "Checking environment health..."
eb health

echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "To view logs: eb logs"
echo "To open app: eb open"
echo "To check status: eb status"
