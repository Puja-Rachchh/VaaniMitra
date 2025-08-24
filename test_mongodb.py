#!/usr/bin/env python3
"""
Test MongoDB Connection and User Creation
"""

from app import app
from mongodb_models import User, mongo

def test_mongodb_connection():
    """Test MongoDB connection and operations"""
    
    with app.app_context():
        try:
            # Test connection
            db_stats = mongo.db.command("dbstats")
            print("✅ MongoDB connection successful!")
            print(f"Database: {db_stats.get('db', 'Unknown')}")
            
            # List existing users
            users = User.get_all_users()
            print(f"📊 Found {len(users)} users in database:")
            for user in users:
                print(f"  - {user.username} (Level: {user.level}, Language: {user.target_language})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing MongoDB: {e}")
            return False

def create_test_user():
    """Create a test user for login testing"""
    
    with app.app_context():
        try:
            # Check if test user exists
            existing_user = User.find_by_username("test")
            if existing_user:
                print("Test user already exists.")
                return
            
            # Create test user
            test_user = User(
                username="test",
                known_language="English",
                target_language="Hindi",
                level="Intermediate"
            )
            test_user.set_password("test123")
            test_user.save()
            
            print("✅ Test user created successfully!")
            print("Username: test")
            print("Password: test123")
            
        except Exception as e:
            print(f"❌ Error creating test user: {e}")

if __name__ == "__main__":
    print("VaaniMitra MongoDB Test")
    print("=" * 30)
    
    if test_mongodb_connection():
        print("\n" + "=" * 30)
        create_test_user()
        
    print("\n" + "=" * 30)
    print("Test completed!")
    print("You can now start the Flask app with: python app.py")
