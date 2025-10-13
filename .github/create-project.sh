#!/bin/bash

# GitHub Projects Setup Script for MedScan Platform
# This script creates a GitHub Project (beta) with predefined columns and settings

set -e

echo "Creating GitHub Project for MedScan Platform..."

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI."
    echo "Run: gh auth login"
    exit 1
fi

# Get repository info
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Repository: $REPO"

# Create the project
echo "Creating project 'MedScan Development'..."
PROJECT_ID=$(gh project create \
    --title "MedScan Development" \
    --owner "$(echo $REPO | cut -d'/' -f1)" \
    --format json | jq -r '.id')

if [ -z "$PROJECT_ID" ]; then
    echo "Error: Failed to create project"
    exit 1
fi

echo "Project created with ID: $PROJECT_ID"

# Note: GitHub CLI currently has limited support for project customization
# Additional configuration should be done via the web interface:
# 1. Add custom fields (Priority, Component, Sprint, Estimate)
# 2. Create views (Backlog, Current Sprint, In Progress, In Review, Done)
# 3. Configure automation rules

echo ""
echo " Project created successfully!"
echo ""
echo "Next steps:"
echo "1. Visit the project: https://github.com/orgs/$(echo $REPO | cut -d'/' -f1)/projects"
echo "2. Add custom fields: Priority, Component, Sprint, Estimate"
echo "3. Create views: Backlog, Current Sprint, In Progress, In Review, Done"
echo "4. Configure automation rules"
echo "5. Link existing issues to the project"
echo ""
echo "For detailed setup instructions, see .github/PROJECT_SETUP.md"
