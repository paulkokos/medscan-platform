#!/bin/bash

set -e

echo "=========================================="
echo "AWS S3 + CloudFront Deployment Script"
echo "=========================================="

BUCKET_NAME=${1:-"medscan-frontend"}
REGION=${2:-"us-east-1"}

cd "$(dirname "$0")/../frontend"

echo "Checking AWS credentials..."
aws sts get-caller-identity > /dev/null 2>&1 || {
    echo "Error: AWS credentials not configured"
    echo "Please run 'aws configure'"
    exit 1
}

echo "Building React application..."
npm run build

echo "Creating S3 bucket if it doesn't exist..."
aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null || \
    aws s3api create-bucket \
        --bucket "$BUCKET_NAME" \
        --region "$REGION" \
        --create-bucket-configuration LocationConstraint="$REGION"

echo "Configuring S3 bucket for static website hosting..."
aws s3 website "s3://$BUCKET_NAME" \
    --index-document index.html \
    --error-document index.html

echo "Setting bucket policy for public read access..."
cat > /tmp/bucket-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
    }
  ]
}
EOF

aws s3api put-bucket-policy \
    --bucket "$BUCKET_NAME" \
    --policy file:///tmp/bucket-policy.json

echo "Uploading files to S3..."
aws s3 sync build/ "s3://$BUCKET_NAME" \
    --delete \
    --cache-control "public, max-age=31536000" \
    --exclude "index.html" \
    --exclude "*.map"

aws s3 cp build/index.html "s3://$BUCKET_NAME/index.html" \
    --cache-control "public, max-age=0, must-revalidate"

echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo ""
echo "Website URL: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo ""
echo "To set up CloudFront CDN:"
echo "1. Go to AWS CloudFront Console"
echo "2. Create a new distribution"
echo "3. Set origin to: $BUCKET_NAME.s3-website-$REGION.amazonaws.com"
