#!/usr/bin/env python3
"""
Data Migration Script: SQLite to MongoDB
This script migrates user data from SQLite to MongoDB for VaaniMitra
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from mongodb_models import User, mongo
from app import app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_users():
    """Migrate users from SQLite to MongoDB"""
    
    # Path to SQLite database
    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    
    if not os.path.exists(sqlite_db_path):
        print("SQLite database not found. No migration needed.")
        return
    
    # Connect to SQLite
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    try:
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user';")
        if not cursor.fetchone():
            print("No users table found in SQLite database.")
            return
        
        # Fetch all users from SQLite
        cursor.execute("SELECT id, username, password, known_language, target_language, level FROM user")
        sqlite_users = cursor.fetchall()
        
        if not sqlite_users:
            print("No users found in SQLite database.")
            return
        
        print(f"Found {len(sqlite_users)} users in SQLite database.")
        
        # Migrate each user to MongoDB
        migrated_count = 0
        skipped_count = 0
        
        with app.app_context():
            for sqlite_user in sqlite_users:
                user_id, username, password, known_language, target_language, level = sqlite_user
                
                # Check if user already exists in MongoDB
                existing_user = User.find_by_username(username)
                if existing_user:
                    print(f"User '{username}' already exists in MongoDB. Skipping.")
                    skipped_count += 1
                    continue
                
                # Create new MongoDB user
                new_user = User(
                    username=username,
                    password=password,  # Password is already hashed in SQLite
                    known_language=known_language,
                    target_language=target_language,
                    level=level
                )
                
                try:
                    new_user.save()
                    print(f"Migrated user: {username}")
                    migrated_count += 1
                except Exception as e:
                    print(f"Error migrating user {username}: {e}")
        
        print(f"\nMigration completed:")
        print(f"- Migrated: {migrated_count} users")
        print(f"- Skipped: {skipped_count} users")
        print(f"- Total processed: {len(sqlite_users)} users")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        conn.close()

def verify_migration():
    """Verify the migration by comparing user counts"""
    
    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    
    if not os.path.exists(sqlite_db_path):
        print("SQLite database not found for verification.")
        return
    
    # Count SQLite users
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM user")
    sqlite_count = cursor.fetchone()[0]
    conn.close()
    
    # Count MongoDB users
    with app.app_context():
        mongodb_users = User.get_all_users()
        mongodb_count = len(mongodb_users)
    
    print(f"\nVerification Results:")
    print(f"- SQLite users: {sqlite_count}")
    print(f"- MongoDB users: {mongodb_count}")
    
    if sqlite_count == mongodb_count:
        print("✅ Migration verification successful!")
    else:
        print("⚠️ User counts don't match. Please check the migration.")

def backup_sqlite():
    """Create a backup of the SQLite database"""
    
    sqlite_db_path = os.path.join(os.path.dirname(__file__), 'users.db')
    backup_path = os.path.join(os.path.dirname(__file__), f'users_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db')
    
    if os.path.exists(sqlite_db_path):
        try:
            import shutil
            shutil.copy2(sqlite_db_path, backup_path)
            print(f"SQLite database backed up to: {backup_path}")
        except Exception as e:
            print(f"Error creating backup: {e}")
    else:
        print("SQLite database not found for backup.")

if __name__ == "__main__":
    print("VaaniMitra Database Migration: SQLite to MongoDB")
    print("=" * 50)
    
    # Create backup first
    print("1. Creating backup of SQLite database...")
    backup_sqlite()
    
    # Perform migration
    print("\n2. Starting migration...")
    migrate_users()
    
    # Verify migration
    print("\n3. Verifying migration...")
    verify_migration()
    
    print("\n" + "=" * 50)
    print("Migration process completed!")
    print("You can now test your application with MongoDB.")
    print("If everything works correctly, you can remove the SQLite database file.")
