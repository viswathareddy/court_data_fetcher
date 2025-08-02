#!/usr/bin/env python3
"""
Debug script to identify Flask application issues
"""

import traceback
import sys

def test_app_creation():
    """Test app creation"""
    try:
        from app import create_app
        app = create_app()
        print("✅ App creation successful")
        return app
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        traceback.print_exc()
        return None

def test_template_rendering(app):
    """Test template rendering"""
    try:
        with app.app_context():
            from flask import render_template
            # Test rendering index template
            result = render_template('index.html')
            print("✅ Template rendering successful")
            return True
    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        traceback.print_exc()
        return False

def test_route_registration(app):
    """Test route registration"""
    try:
        routes = list(app.url_map.iter_rules())
        print(f"✅ Routes registered: {len(routes)} routes found")
        for route in routes:
            print(f"   - {route}")
        return True
    except Exception as e:
        print(f"❌ Route registration failed: {e}")
        traceback.print_exc()
        return False

def test_database_connection(app):
    """Test database connection"""
    try:
        with app.app_context():
            from app import db
            from app.models import QueryLog
            count = QueryLog.query.count()
            print(f"✅ Database connection successful: {count} records")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all debug tests"""
    print("🔍 Debugging Flask Application")
    print("=" * 40)
    
    # Test app creation
    app = test_app_creation()
    if not app:
        return
    
    # Test route registration
    test_route_registration(app)
    
    # Test template rendering
    test_template_rendering(app)
    
    # Test database connection
    test_database_connection(app)
    
    print("\n✅ Debug complete!")

if __name__ == "__main__":
    main() 