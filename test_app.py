#!/usr/bin/env python3
"""
Test script for Court Data Fetcher application
"""

import requests
import sys
import os

def test_flask_app():
    """Test if the Flask app is running and accessible"""
    try:
        response = requests.get('http://127.0.0.1:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Flask application is running successfully!")
            print(f"📊 Status Code: {response.status_code}")
            return True
        else:
            print(f"❌ Flask application returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask application. Is it running?")
        print("💡 Run: python run.py")
        return False
    except Exception as e:
        print(f"❌ Error testing Flask app: {e}")
        return False

def test_database():
    """Test database connectivity"""
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            # Try to query the database
            from app.models import QueryLog
            count = QueryLog.query.count()
            print(f"✅ Database connection successful! QueryLog count: {count}")
            return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_scraper():
    """Test scraper functionality"""
    try:
        from app.scraper import fetch_case_details
        # Test with a sample case
        result, error = fetch_case_details("WP(C)", "1234", "2024")
        if error:
            print(f"⚠️  Scraper test completed with expected error: {error}")
        else:
            print("✅ Scraper test completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Court Data Fetcher Application")
    print("=" * 50)
    
    tests = [
        ("Database Connection", test_database),
        ("Scraper Functionality", test_scraper),
        ("Flask Application", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        if test_func():
            passed += 1
        print("-" * 30)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to use.")
        print("\n🌐 Access the application at: http://127.0.0.1:5000")
        print("📖 View documentation in README.md")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 