# Performance Metrics Guide for Online Bookstore Flask App

This guide explains how to monitor and analyze performance metrics for your Flask application.

## 🚀 Quick Start - View Performance Metrics

### Method 1: Web Dashboard (Recommended)
1. Start your Flask app: `python app.py`
2. Open your browser and go to: `http://127.0.0.1:5000/dashboard`
3. Use the application (browse books, add to cart, etc.)
4. Refresh the dashboard to see updated metrics

### Method 2: JSON API Endpoint
- **Metrics API**: `http://127.0.0.1:5000/metrics`
- **Health Check**: `http://127.0.0.1:5000/health`

### Method 3: Command Line Monitor
```bash
python simple_monitor.py
```

## 📊 Available Metrics

### 1. **Request Metrics**
- Total number of requests processed
- Average response time across all requests
- Request count and timing per route

### 2. **Route Performance**
- Individual route statistics (count, average time, total time)
- Response time tracking for each endpoint
- Performance comparison between different routes

### 3. **Application Health**
- Server status and uptime
- Timestamp of last health check
- Application availability monitoring

## 🔧 Performance Monitoring Features

### Built-in Flask Profiler
The app includes Werkzeug's ProfilerMiddleware in debug mode:
- Automatically profiles each request
- Saves profile data to `./profiles/` directory
- Detailed function-level performance analysis

### Request/Response Logging
Every request is logged with:
- HTTP method and path
- Response status code  
- Response time in milliseconds
- Timestamp

### Performance Statistics Collection
The app tracks:
- Global request count and response times
- Per-route performance statistics
- Real-time averages and totals

## 📈 How to Use the Metrics

### 1. **Identify Slow Routes**
Look for routes with high average response times in the dashboard:
```
Route               Count    Avg Time
index               45       12.34ms
add_to_cart         23       8.91ms
checkout            12       15.67ms  ← This might need optimization
```

### 2. **Monitor Application Load**
Watch the total request count and overall average response time:
- Sudden spikes might indicate performance issues
- Gradual increases suggest growing usage

### 3. **Performance Testing**
Use the included performance test script:
```bash
python performance_test.py
```

This script will:
- Simulate realistic user behavior
- Generate load on your application
- Provide detailed performance analysis
- Show percentile response times (50th, 90th, 95th)

## 🛠️ Advanced Performance Monitoring

### 1. **Profile Analysis**
When running in debug mode, profile files are saved to `./profiles/`:
```bash
# View profile files (if snakeviz is installed)
pip install snakeviz
snakeviz profiles/GET.127.0.0.1.5000.001.prof
```

### 2. **Custom Performance Logging**
Add the `@log_performance` decorator to any function:
```python
@log_performance
def my_slow_function():
    # Your code here
    pass
```

### 3. **Memory and CPU Monitoring**
For system-level monitoring, consider adding:
```python
import psutil
import os

@app.route('/system-metrics')
def system_metrics():
    process = psutil.Process(os.getpid())
    return jsonify({
        'cpu_percent': process.cpu_percent(),
        'memory_mb': process.memory_info().rss / 1024 / 1024,
        'memory_percent': process.memory_percent()
    })
```

## 📝 Performance Best Practices

### 1. **Baseline Measurement**
- Run performance tests before making changes
- Establish baseline metrics for comparison
- Monitor trends over time

### 2. **Load Testing**
- Test with realistic user loads
- Identify breaking points and bottlenecks
- Verify performance under stress

### 3. **Continuous Monitoring**
- Check metrics regularly during development
- Set up alerts for performance degradation
- Monitor production deployments

### 4. **Optimization Targets**
- **Good**: < 100ms average response time
- **Acceptable**: 100-500ms average response time  
- **Needs attention**: > 500ms average response time

## 🚨 Troubleshooting Performance Issues

### Common Issues and Solutions

1. **High Response Times**
   - Check for database queries (if added later)
   - Look for CPU-intensive operations
   - Consider caching frequently accessed data

2. **Memory Issues**
   - Monitor memory usage in system metrics
   - Check for memory leaks in long-running processes
   - Consider pagination for large data sets

3. **Slow Route Performance**
   - Use the profiler to identify bottlenecks
   - Optimize expensive operations
   - Consider async processing for heavy tasks

### Performance Testing Checklist

- [ ] Measure baseline performance
- [ ] Test with concurrent users
- [ ] Monitor response time percentiles
- [ ] Check for memory leaks
- [ ] Verify under different loads
- [ ] Test error scenarios
- [ ] Monitor over extended periods

## 🔗 Integration with CI/CD

### Azure DevOps Integration
Add performance tests to your pipeline:
```yaml
- task: PythonScript@0
  displayName: 'Run Performance Tests'
  inputs:
    scriptSource: 'filePath'
    scriptPath: 'performance_test.py'
    
- task: PublishTestResults@2
  displayName: 'Publish Performance Results'
  inputs:
    testResultsFiles: 'performance-results.xml'
    testRunTitle: 'Performance Tests'
```

### Docker Monitoring
When using Docker, monitor container metrics:
```bash
docker stats
docker exec -it <container> python simple_monitor.py
```

## 📚 Next Steps

1. **Start monitoring** your application with the dashboard
2. **Run performance tests** to establish baselines
3. **Identify bottlenecks** using the profiler
4. **Optimize** slow routes and functions
5. **Set up alerts** for production monitoring
6. **Integrate** performance testing into your CI/CD pipeline

## 🔍 Additional Resources

- [Flask Performance Tips](https://flask.palletsprojects.com/en/2.3.x/deploying/#performance)
- [Werkzeug Profiler Documentation](https://werkzeug.palletsprojects.com/en/2.3.x/middleware/profiler/)
- [Python Performance Profiling](https://docs.python.org/3/library/profile.html)

---

For questions or issues with performance monitoring, check the logs or contact your development team.