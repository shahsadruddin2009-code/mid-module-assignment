#!/bin/bash
# 🔧 Utilities Script for GitHub Actions
# Common utility functions used across different workflows

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }
print_debug() { echo -e "${PURPLE}[DEBUG]${NC} $1"; }
print_step() { echo -e "${CYAN}[STEP]${NC} $1"; }

# Function to create a banner
print_banner() {
    local message="$1"
    local length=${#message}
    local border=$(printf "%-${length}s" "=" | tr ' ' '=')
    
    echo -e "${BLUE}"
    echo "╔═$border═╗"
    echo "║ $message ║"
    echo "╚═$border═╝"
    echo -e "${NC}"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Python version
check_python_version() {
    local min_version="$1"
    if ! command_exists python; then
        print_error "Python is not installed"
        return 1
    fi
    
    local current_version=$(python --version 2>&1 | cut -d' ' -f2)
    print_status "Current Python version: $current_version"
    
    # Simple version comparison (assumes semantic versioning)
    if [[ "$current_version" < "$min_version" ]]; then
        print_warning "Python version $current_version is below minimum required $min_version"
        return 1
    fi
    
    print_success "Python version requirement met"
    return 0
}

# Function to validate environment variables
validate_env_vars() {
    local vars=("$@")
    local missing_vars=()
    
    for var in "${vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -eq 0 ]; then
        print_success "All required environment variables are set"
        return 0
    else
        print_error "Missing required environment variables: ${missing_vars[*]}"
        return 1
    fi
}

# Function to create directory structure
create_directories() {
    local dirs=("$@")
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            print_status "Created directory: $dir"
        else
            print_debug "Directory already exists: $dir"
        fi
    done
}

# Function to backup file
backup_file() {
    local file="$1"
    local backup_dir="${2:-backups}"
    
    if [ -f "$file" ]; then
        local timestamp=$(date +"%Y%m%d_%H%M%S")
        local backup_name="${backup_dir}/$(basename "$file").backup_$timestamp"
        
        mkdir -p "$backup_dir"
        cp "$file" "$backup_name"
        print_success "Backed up $file to $backup_name"
    else
        print_warning "File $file not found, skipping backup"
    fi
}

# Function to check disk space
check_disk_space() {
    local min_space_gb="${1:-1}"
    local available_gb=$(df . | awk 'NR==2 {print int($4/1024/1024)}')
    
    print_status "Available disk space: ${available_gb}GB"
    
    if [ "$available_gb" -lt "$min_space_gb" ]; then
        print_error "Insufficient disk space. Available: ${available_gb}GB, Required: ${min_space_gb}GB"
        return 1
    fi
    
    print_success "Sufficient disk space available"
    return 0
}

# Function to check network connectivity
check_connectivity() {
    local urls=("$@")
    local failed=0
    
    for url in "${urls[@]}"; do
        print_status "Checking connectivity to $url..."
        if curl -s --max-time 10 --head "$url" > /dev/null; then
            print_success "✅ $url is reachable"
        else
            print_error "❌ $url is not reachable"
            ((failed++))
        fi
    done
    
    if [ $failed -eq 0 ]; then
        print_success "All connectivity checks passed"
        return 0
    else
        print_error "$failed connectivity checks failed"
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url="$1"
    local timeout="${2:-60}"
    local interval="${3:-5}"
    local elapsed=0
    
    print_status "Waiting for service at $url to be ready (timeout: ${timeout}s)..."
    
    while [ $elapsed -lt $timeout ]; do
        if curl -s --max-time 5 "$url" > /dev/null 2>&1; then
            print_success "Service is ready!"
            return 0
        fi
        
        sleep $interval
        elapsed=$((elapsed + interval))
        print_debug "Waiting... (${elapsed}/${timeout}s)"
    done
    
    print_error "Service did not become ready within ${timeout}s"
    return 1
}

# Function to retry command with exponential backoff
retry_command() {
    local max_attempts="$1"
    local delay="$2"
    shift 2
    local command=("$@")
    
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_status "Attempt $attempt/$max_attempts: ${command[*]}"
        
        if "${command[@]}"; then
            print_success "Command succeeded on attempt $attempt"
            return 0
        fi
        
        if [ $attempt -lt $max_attempts ]; then
            print_warning "Command failed, retrying in ${delay}s..."
            sleep $delay
            delay=$((delay * 2))  # Exponential backoff
        fi
        
        ((attempt++))
    done
    
    print_error "Command failed after $max_attempts attempts"
    return 1
}

# Function to generate random string
generate_random_string() {
    local length="${1:-16}"
    local charset="${2:-A-Za-z0-9}"
    
    tr -dc "$charset" < /dev/urandom | head -c "$length"
}

# Function to calculate file checksum
calculate_checksum() {
    local file="$1"
    local algorithm="${2:-sha256}"
    
    if [ ! -f "$file" ]; then
        print_error "File not found: $file"
        return 1
    fi
    
    case $algorithm in
        "md5")
            md5sum "$file" | cut -d' ' -f1
            ;;
        "sha1")
            sha1sum "$file" | cut -d' ' -f1
            ;;
        "sha256")
            sha256sum "$file" | cut -d' ' -f1
            ;;
        *)
            print_error "Unsupported algorithm: $algorithm"
            return 1
            ;;
    esac
}

# Function to compress directory
compress_directory() {
    local source_dir="$1"
    local output_file="$2"
    local compression="${3:-gz}"
    
    if [ ! -d "$source_dir" ]; then
        print_error "Source directory not found: $source_dir"
        return 1
    fi
    
    case $compression in
        "gz"|"gzip")
            tar -czf "$output_file" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
            ;;
        "bz2"|"bzip2")
            tar -cjf "$output_file" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
            ;;
        "xz")
            tar -cJf "$output_file" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
            ;;
        *)
            print_error "Unsupported compression: $compression"
            return 1
            ;;
    esac
    
    print_success "Compressed $source_dir to $output_file"
}

# Function to send notification (generic)
send_notification() {
    local title="$1"
    local message="$2"
    local webhook_url="${3:-$NOTIFICATION_WEBHOOK_URL}"
    
    if [ -z "$webhook_url" ]; then
        print_warning "No webhook URL provided for notification"
        return 0
    fi
    
    local payload=$(cat <<EOF
{
    "title": "$title",
    "message": "$message",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
)
    
    if curl -s -H "Content-Type: application/json" -d "$payload" "$webhook_url" > /dev/null; then
        print_success "Notification sent successfully"
    else
        print_warning "Failed to send notification"
    fi
}

# Function to cleanup temporary files
cleanup_temp_files() {
    local temp_patterns=("$@")
    
    if [ ${#temp_patterns[@]} -eq 0 ]; then
        temp_patterns=("*.tmp" "*.temp" ".temp*" "temp_*")
    fi
    
    for pattern in "${temp_patterns[@]}"; do
        local files=($(find . -name "$pattern" -type f 2>/dev/null))
        if [ ${#files[@]} -gt 0 ]; then
            print_status "Cleaning up files matching: $pattern"
            rm -f "${files[@]}"
            print_success "Removed ${#files[@]} temporary files"
        fi
    done
}

# Function to get system information
get_system_info() {
    print_banner "System Information"
    echo "OS: $(uname -s)"
    echo "Architecture: $(uname -m)"
    echo "Kernel: $(uname -r)"
    echo "Hostname: $(hostname)"
    echo "Date: $(date)"
    echo "Uptime: $(uptime)"
    echo "Disk Usage: $(df -h . | awk 'NR==2 {print $3"/"$2" ("$5" used)"}')"
    echo "Memory Usage: $(free -h 2>/dev/null | awk 'NR==2{print $3"/"$2}' || echo 'N/A')"
    echo "CPU Cores: $(nproc 2>/dev/null || echo 'N/A')"
}

# Function to validate JSON
validate_json() {
    local json_file="$1"
    
    if [ ! -f "$json_file" ]; then
        print_error "JSON file not found: $json_file"
        return 1
    fi
    
    if command_exists jq; then
        if jq empty "$json_file" 2>/dev/null; then
            print_success "JSON file is valid: $json_file"
            return 0
        else
            print_error "JSON file is invalid: $json_file"
            return 1
        fi
    else
        print_warning "jq not available, skipping JSON validation"
        return 0
    fi
}

# Help function
show_utils_help() {
    cat << EOF
🔧 GitHub Actions Utilities Script

Available Functions:
  print_*                 - Colored logging functions
  print_banner           - Create formatted banners
  command_exists         - Check if command is available
  check_python_version   - Validate Python version
  validate_env_vars      - Check required environment variables
  create_directories     - Create directory structure
  backup_file           - Backup files with timestamps
  check_disk_space      - Validate available disk space
  check_connectivity    - Test network connectivity
  wait_for_service      - Wait for service to be ready
  retry_command         - Retry commands with backoff
  generate_random_string - Generate random strings
  calculate_checksum    - Calculate file checksums
  compress_directory    - Create compressed archives
  send_notification     - Send webhook notifications
  cleanup_temp_files    - Clean temporary files
  get_system_info       - Display system information
  validate_json         - Validate JSON files

Usage:
  source .github/scripts/utils.sh
  print_banner "My Banner"
  check_python_version "3.8"
  validate_env_vars "VAR1" "VAR2"

EOF
}

# If script is run directly, show help
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    show_utils_help
fi