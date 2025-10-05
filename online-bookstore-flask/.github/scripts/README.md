# 🛠️ GitHub Actions Shell Scripts

This directory contains modular shell scripts for your GitHub Actions workflows, designed to make your CI/CD pipelines more maintainable and reusable.

## 📁 Available Scripts

### 🚀 `setup-environment.sh`
**Purpose:** Environment setup and dependency installation
**Usage in Workflow:**
```yaml
- name: Setup Environment
  run: bash .github/scripts/setup-environment.sh
```
**Features:**
- Python version validation
- Production & development dependency installation
- Additional CI/CD tools installation
- Colored output and error handling

### 🧪 `run-tests.sh`
**Purpose:** Comprehensive test suite execution
**Usage in Workflow:**
```yaml
- name: Run Tests
  run: bash .github/scripts/run-tests.sh
```
**Features:**
- Unit, integration, and performance tests
- Code coverage reporting (XML, HTML, Terminal)
- JUnit XML output for CI integration
- Test summary generation
- Configurable coverage thresholds

### 🛡️ `security-scan.sh`
**Purpose:** Security vulnerability scanning
**Usage in Workflow:**
```yaml
- name: Security Scan
  run: bash .github/scripts/security-scan.sh
```
**Features:**
- Bandit Python AST security scanner
- Safety dependency vulnerability checker
- Hardcoded secrets detection
- Security configuration checks
- Comprehensive security reporting

### 🚀 `deploy.sh`
**Purpose:** Blue-green deployment with health checks
**Usage in Workflow:**
```yaml
- name: Deploy to Staging
  run: bash .github/scripts/deploy.sh staging ${{ github.sha }}
- name: Deploy to Production
  run: bash .github/scripts/deploy.sh production ${{ github.ref_name }}
```
**Features:**
- Blue-green deployment strategy
- Health check validation
- Smoke tests
- Rollback capabilities
- Deployment record keeping

### 📊 `performance-test.sh`
**Purpose:** Performance testing with Locust
**Usage in Workflow:**
```yaml
- name: Performance Test
  run: bash .github/scripts/performance-test.sh http://localhost:5000 50 10 5m
```
**Parameters:**
1. Target URL (default: http://localhost:5000)
2. Concurrent Users (default: 50)
3. Spawn Rate (default: 10)
4. Duration (default: 5m)

**Features:**
- Locust-based load testing
- Multiple test scenarios (homepage, search, cart, etc.)
- Performance threshold validation
- Comprehensive reporting
- Local app startup/shutdown

### 🔧 `utils.sh`
**Purpose:** Common utility functions
**Usage in Workflow:**
```yaml
- name: Setup Utils
  run: source .github/scripts/utils.sh
```
**Available Functions:**
- Colored logging (`print_status`, `print_success`, `print_error`)
- System checks (`check_python_version`, `check_connectivity`)
- File operations (`backup_file`, `compress_directory`)
- Retry logic (`retry_command`)
- And many more utilities

## 🔧 Integration Examples

### Basic CI Workflow
```yaml
name: CI Pipeline
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Environment
      run: bash .github/scripts/setup-environment.sh
    - name: Run Tests
      run: bash .github/scripts/run-tests.sh
    - name: Security Scan
      run: bash .github/scripts/security-scan.sh
```

### Performance Testing Workflow
```yaml
name: Performance Tests
on:
  workflow_dispatch:
    inputs:
      users:
        description: 'Number of concurrent users'
        default: '50'
      duration:
        description: 'Test duration'
        default: '5m'

jobs:
  performance:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Setup Environment
      run: bash .github/scripts/setup-environment.sh
    - name: Performance Test
      run: bash .github/scripts/performance-test.sh http://localhost:5000 ${{ github.event.inputs.users }} 10 ${{ github.event.inputs.duration }}
```

### Deployment Workflow
```yaml
name: Deploy
on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Deploy to Production
      run: bash .github/scripts/deploy.sh production ${{ github.event.release.tag_name }}
```

## 📊 Generated Reports and Artifacts

### Test Results
- `test-results/junit.xml` - JUnit XML for CI integration
- `coverage.xml` - Coverage report in XML format
- `htmlcov/` - HTML coverage reports
- `test-results/summary.md` - Test execution summary

### Security Reports
- `security-results/bandit-report.json` - Bandit security scan results
- `security-results/safety-report.json` - Dependency vulnerability report
- `security-results/security-summary.md` - Comprehensive security summary

### Performance Reports
- `performance-results/performance-report.html` - Locust HTML report
- `performance-results/performance-summary.json` - Performance metrics
- `performance-results/performance-*.csv` - Raw performance data

### Deployment Records
- `deployment-records/deployment-{env}-{timestamp}.json` - Deployment tracking
- `deployment-summary.md` - Deployment summary and verification

## 🎯 Best Practices

### 1. Error Handling
All scripts use `set -e` to exit on errors and include comprehensive error checking.

### 2. Colored Output
Consistent colored output using utility functions:
- 🔵 **Blue** - Info/Status messages
- 🟢 **Green** - Success messages
- 🟡 **Yellow** - Warning messages
- 🔴 **Red** - Error messages

### 3. Configurable Parameters
Scripts accept parameters for customization while providing sensible defaults.

### 4. Artifact Generation
All scripts generate reports and artifacts suitable for CI/CD integration.

### 5. Modular Design
Each script focuses on a specific concern and can be used independently.

## 🔧 Customization

### Environment Variables
Scripts respect common environment variables:
- `GITHUB_ACTOR` - GitHub username
- `GITHUB_RUN_ID` - Workflow run ID  
- `GITHUB_REPOSITORY` - Repository name
- `NOTIFICATION_WEBHOOK_URL` - Webhook for notifications

### Configuration Files
- `.bandit` - Bandit security scanner configuration
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies

### Thresholds
Modify threshold values in scripts:
- **Coverage:** `TEST_COVERAGE_THRESHOLD=80`
- **Performance:** `MAX_RESPONSE_TIME=2000`
- **Error Rate:** `MAX_ERROR_RATE=0.05`

## 🚀 Getting Started

1. **Make scripts executable** (Linux/macOS):
   ```bash
   chmod +x .github/scripts/*.sh
   ```

2. **Test locally**:
   ```bash
   bash .github/scripts/setup-environment.sh
   bash .github/scripts/run-tests.sh
   ```

3. **Integrate into workflows**:
   - Copy examples above into `.github/workflows/`
   - Customize parameters as needed
   - Add artifact uploading for reports

4. **Monitor results**:
   - Check workflow logs for colored output
   - Download generated reports from artifacts
   - Review security and performance summaries

---

*These scripts are designed to work with the Online Bookstore Flask application and can be adapted for other Python projects.*