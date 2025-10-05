#!/usr/bin/env python3
"""
Simple Performance Monitor for Online Bookstore
This script monitors the Flask app without external dependencies
"""

import urllib.request
import json
import time
import threading

class SimpleMonitor:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.is_monitoring = False
        
    def check_health(self):
        """Check if the server is healthy"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/health") as response:
                data = json.loads(response.read().decode())
                return True, data
        except Exception as e:
            return False, str(e)
    
    def get_metrics(self):
        """Get current performance metrics"""
        try:
            with urllib.request.urlopen(f"{self.base_url}/metrics") as response:
                data = json.loads(response.read().decode())
                return True, data
        except Exception as e:
            return False, str(e)
    
    def display_metrics(self, metrics):
        """Display metrics in a formatted way"""
        print("\n" + "="*50)
        print(f"📊 PERFORMANCE METRICS - {time.strftime('%H:%M:%S')}")
        print("="*50)
        
        print(f"🔢 Total Requests: {metrics.get('total_requests', 0)}")
        print(f"⏱️  Average Response Time: {metrics.get('average_response_time', 'N/A')}")
        
        route_stats = metrics.get('route_statistics', {})
        if route_stats:
            print(f"\n📍 Route Performance:")
            print(f"{'Route':<20} {'Count':<8} {'Avg Time':<12}")
            print("-" * 40)
            for route, stats in route_stats.items():
                print(f"{route:<20} {stats['count']:<8} {stats['avg_time']:<10.2f}ms")
    
    def start_monitoring(self, interval=10):
        """Start continuous monitoring"""
        print(f"🚀 Starting performance monitoring (refresh every {interval}s)")
        print(f"📈 Dashboard available at: {self.base_url}/dashboard")
        print("Press Ctrl+C to stop monitoring\n")
        
        self.is_monitoring = True
        
        try:
            while self.is_monitoring:
                # Check health
                health_ok, health_data = self.check_health()
                if not health_ok:
                    print(f"❌ Health check failed: {health_data}")
                    time.sleep(interval)
                    continue
                
                # Get and display metrics
                success, metrics = self.get_metrics()
                if success:
                    self.display_metrics(metrics)
                else:
                    print(f"❌ Failed to get metrics: {metrics}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
            self.is_monitoring = False

def main():
    """Main function"""
    print("📊 Online Bookstore Performance Monitor")
    print("="*40)
    
    monitor = SimpleMonitor()
    
    # Test connection
    print("🔍 Testing connection to Flask app...")
    health_ok, health_data = monitor.check_health()
    
    if not health_ok:
        print("❌ Cannot connect to Flask app!")
        print("Please start the app first with: python app.py")
        return
    
    print("✅ Connection successful!")
    print(f"🏥 Health status: {health_data}")
    
    # Start monitoring
    monitor.start_monitoring()

if __name__ == "__main__":
    main()