#!/bin/bash
# 🐍 PythonAnywhere Deployment Script
# Deploy Online Bookstore Flask App to PythonAnywhere

set -e

echo "🐍 PythonAnywhere Deployment Script"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
PYTHONANYWHERE_USERNAME="shahsadruddin2009"
PROJECT_PATH="/home/${PYTHONANYWHERE_USERNAME}/mid-module-assignment/online-bookstore-flask"
PYTHON_VERSION="python3.10"

print_status "Starting PythonAnywhere deployment..."

# Check if we're on PythonAnywhere
if [[ ! -f /etc/pythonanywhere_domain ]]; then
    print_warning "This script is designed to run on PythonAnywhere servers"
fi

# Navigate to project directory
if [ -d "$PROJECT_PATH" ]; then
    print_status "Navigating to project directory: $PROJECT_PATH"
    cd "$PROJECT_PATH"
else
    print_error "Project directory not found: $PROJECT_PATH"
    print_status "Please clone your repository first:"
    echo "  git clone https://github.com/shahsadruddin2009-code/mid-module-assignment.git"
    exit 1
fi

# Pull latest changes
print_status "Pulling latest changes from Git..."
if git pull origin main; then
    print_success "Git pull completed successfully"
else
    print_warning "Git pull failed or no changes to pull"
fi

# Install/Update dependencies
print_status "Installing Python dependencies..."
if ${PYTHON_VERSION} -m pip install --user -r requirements.txt; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Run tests (optional)
print_status "Running quick tests..."
if ${PYTHON_VERSION} -m pytest --version > /dev/null 2>&1; then
    if ${PYTHON_VERSION} -m pytest test_app_model.py -v; then
        print_success "Tests passed"
    else
        print_warning "Some tests failed, but continuing deployment"
    fi
else
    print_warning "pytest not available, skipping tests"
fi

# Create/Update WSGI file content
print_status "Generating WSGI configuration..."
WSGI_CONTENT="import sys
import os

# Add your project directory to Python path
project_home = '$PROJECT_PATH'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'production'

# Import your Flask app
from app import app as application

if __name__ == \"__main__\":
    application.run()"

echo "$WSGI_CONTENT" > wsgi_config_template.py
print_success "WSGI configuration template created: wsgi_config_template.py"

# Test application locally
print_status "Testing application configuration..."
if ${PYTHON_VERSION} -c "from app import app; print('✅ Flask app imports successfully')"; then
    print_success "Application configuration is valid"
else
    print_error "Application configuration has issues"
    exit 1
fi

# Display post-deployment instructions
print_success "🎉 Deployment preparation completed!"
echo ""
print_status "Next steps:"
echo "1. Go to PythonAnywhere Web tab: https://www.pythonanywhere.com/user/${PYTHONANYWHERE_USERNAME}/webapps/"
echo "2. Copy the WSGI configuration from: wsgi_config_template.py"
echo "3. Paste it into your WSGI configuration file"
echo "4. Set static files mapping:"
echo "   - URL: /static/"
echo "   - Directory: ${PROJECT_PATH}/static/"
echo "5. Click 'Reload' to restart your web app"
echo ""
print_success "Your app will be available at: https://${PYTHONANYWHERE_USERNAME}.pythonanywhere.com"

# Health check URLs
echo ""
print_status "Health check endpoints:"
echo "  - https://${PYTHONANYWHERE_USERNAME}.pythonanywhere.com/health"
echo "  - https://${PYTHONANYWHERE_USERNAME}.pythonanywhere.com/metrics"
echo ""

print_success "Deployment script completed! 🚀"