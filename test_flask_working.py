#!/usr/bin/env python3
"""
Test script to verify Flask app is working correctly
"""

import requests
import time
from app import app
import threading
from werkzeug.serving import make_server

def test_flask_app():
    """Test Flask app functionality"""
    print("🚀 Testing Flask App Functionality...")
    
    # Test 1: App Import and Creation
    try:
        from app import app
        print("✅ Flask app imported successfully")
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    # Test 2: Test Client Functionality
    try:
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Test homepage
        response = client.get('/')
        assert response.status_code == 200
        print("✅ Homepage loads successfully (200 OK)")
        
        # Test categories
        response = client.get('/categories')
        assert response.status_code == 200
        print("✅ Categories page loads successfully (200 OK)")
        
        # Test cart
        response = client.get('/cart')
        assert response.status_code == 200
        print("✅ Cart page loads successfully (200 OK)")
        
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200
        print("✅ Health endpoint working (200 OK)")
        
    except Exception as e:
        print(f"❌ Flask test client failed: {e}")
        return False
    
    # Test 3: Routes Configuration
    try:
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/categories', '/cart', '/health', '/metrics']
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} configured correctly")
            else:
                print(f"⚠️  Route {route} not found")
        
    except Exception as e:
        print(f"❌ Route configuration test failed: {e}")
        return False
    
    print("\n🎉 Flask App is working correctly!")
    print(f"📊 Total configured routes: {len(routes)}")
    print(f"🔧 Available routes: {routes}")
    
    return True

if __name__ == "__main__":
    test_flask_app()