#!/bin/bash
# 🛠️ Environment Setup Script for GitHub Actions
# Sets up the development environment with all necessary dependencies

set -e  # Exit on error

echo "🚀 Setting up environment for Online Bookstore Flask App"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
python_version=$(python --version 2>&1)
print_success "Python version: $python_version"

# Upgrade pip
print_status "Upgrading pip..."
python -m pip install --upgrade pip

# Install production dependencies
print_status "Installing production dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Production dependencies installed"
else
    print_error "requirements.txt not found!"
    exit 1
fi

# Install development dependencies
print_status "Installing development dependencies..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt
    print_success "Development dependencies installed"
else
    print_warning "requirements-dev.txt not found, skipping dev dependencies"
fi

# Install additional testing tools
print_status "Installing additional testing and CI tools..."
pip install pytest pytest-cov pytest-benchmark bandit safety flake8 black mypy

print_success "Environment setup completed successfully! ✅"