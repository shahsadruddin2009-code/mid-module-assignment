#!/usr/bin/env python3
"""
Performance Testing Script for Online Bookstore
This script generates sample traffic to test performance monitoring
"""

import requests
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import json

class PerformanceTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def make_request(self, endpoint, method='GET', data=None):
        """Make a request and return response time"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method == 'GET':
                response = self.session.get(url)
            elif method == 'POST':
                response = self.session.post(url, data=data)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to ms
            
            return {
                'endpoint': endpoint,
                'status_code': response.status_code,
                'response_time': response_time,
                'success': response.status_code < 400
            }
        except Exception as e:
            return {
                'endpoint': endpoint,
                'status_code': 0,
                'response_time': 0,
                'success': False,
                'error': str(e)
            }
    
    def simulate_user_session(self):
        """Simulate a typical user browsing session"""
        results = []
        
        # Visit home page
        results.append(self.make_request('/'))
        time.sleep(random.uniform(0.5, 2.0))
        
        # Browse categories
        categories = ['Fiction', 'Dystopia', 'Traditional', 'Adventure']
        category = random.choice(categories)
        results.append(self.make_request(f'/category/{category}'))
        time.sleep(random.uniform(0.5, 1.5))
        
        # Add item to cart (simulate)
        books = ['The Great Gatsby', '1984', 'I Ching', 'Moby Dick']
        book = random.choice(books)
        results.append(self.make_request('/add-to-cart', 'POST', {'book_title': book}))
        time.sleep(random.uniform(0.3, 1.0))
        
        # View cart
        results.append(self.make_request('/cart'))
        time.sleep(random.uniform(0.5, 1.0))
        
        # Maybe checkout (50% chance)
        if random.random() > 0.5:
            results.append(self.make_request('/checkout'))
        
        return results
    
    def run_load_test(self, num_users=10, duration=60):
        """Run a load test with multiple concurrent users"""
        print(f"Starting load test with {num_users} concurrent users for {duration} seconds")
        
        start_time = time.time()
        all_results = []
        
        def worker():
            user_results = []
            while time.time() - start_time < duration:
                session_results = self.simulate_user_session()
                user_results.extend(session_results)
                time.sleep(random.uniform(1, 3))  # Think time between sessions
            return user_results
        
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [executor.submit(worker) for _ in range(num_users)]
            
            for future in futures:
                results = future.result()
                all_results.extend(results)
        
        return self.analyze_results(all_results)
    
    def analyze_results(self, results):
        """Analyze performance test results"""
        if not results:
            return {}
        
        successful_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]
        
        # Calculate statistics
        response_times = [r['response_time'] for r in successful_results]
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            # Calculate percentiles
            sorted_times = sorted(response_times)
            p50 = sorted_times[len(sorted_times) // 2]
            p90 = sorted_times[int(len(sorted_times) * 0.9)]
            p95 = sorted_times[int(len(sorted_times) * 0.95)]
        else:
            avg_response_time = min_response_time = max_response_time = p50 = p90 = p95 = 0
        
        # Group by endpoint
        endpoint_stats = {}
        for result in successful_results:
            endpoint = result['endpoint']
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = []
            endpoint_stats[endpoint].append(result['response_time'])
        
        # Calculate per-endpoint averages
        for endpoint, times in endpoint_stats.items():
            endpoint_stats[endpoint] = {
                'count': len(times),
                'avg_time': sum(times) / len(times),
                'min_time': min(times),
                'max_time': max(times)
            }
        
        return {
            'total_requests': len(results),
            'successful_requests': len(successful_results),
            'failed_requests': len(failed_results),
            'success_rate': len(successful_results) / len(results) * 100 if results else 0,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p50_response_time': p50,
            'p90_response_time': p90,
            'p95_response_time': p95,
            'endpoint_statistics': endpoint_stats
        }
    
    def get_current_metrics(self):
        """Get current metrics from the application"""
        try:
            response = self.session.get(f"{self.base_url}/metrics")
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error fetching metrics: {e}")
        return {}

def main():
    """Main function to run performance tests"""
    print("Online Bookstore Performance Tester")
    print("=" * 40)
    
    tester = PerformanceTester()
    
    # Test if server is running
    try:
        response = tester.session.get(tester.base_url)
        if response.status_code != 200:
            print("Server is not responding. Please start the Flask app first.")
            return
    except Exception as e:
        print(f"Cannot connect to server: {e}")
        print("Please start the Flask app first with: python app.py")
        return
    
    print("Server is running. Starting performance tests...")
    
    # Run a quick test first
    print("\n1. Running quick test (5 users, 30 seconds)...")
    results = tester.run_load_test(num_users=5, duration=30)
    
    print(f"\nQuick Test Results:")
    print(f"Total Requests: {results['total_requests']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Average Response Time: {results['avg_response_time']:.2f}ms")
    print(f"90th Percentile: {results['p90_response_time']:.2f}ms")
    print(f"95th Percentile: {results['p95_response_time']:.2f}ms")
    
    # Show endpoint statistics
    print(f"\nPer-Endpoint Statistics:")
    for endpoint, stats in results['endpoint_statistics'].items():
        print(f"  {endpoint}: {stats['count']} requests, {stats['avg_time']:.2f}ms avg")
    
    # Get server metrics
    print(f"\n2. Current Server Metrics:")
    server_metrics = tester.get_current_metrics()
    if server_metrics:
        print(f"Total Server Requests: {server_metrics.get('total_requests', 0)}")
        print(f"Server Average Response Time: {server_metrics.get('average_response_time', 'N/A')}")
    
    print(f"\n3. Access the metrics dashboard at: {tester.base_url}/dashboard")
    print(f"4. Raw metrics JSON at: {tester.base_url}/metrics")

if __name__ == "__main__":
    main()