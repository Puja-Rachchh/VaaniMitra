#!/usr/bin/env python3
"""
Session Cleanup Script
This script clears old session data to prevent conflicts after migration
"""

import os
import glob

def clear_flask_sessions():
    """Clear Flask session files"""
    
    # Common Flask session storage locations
    session_paths = [
        'flask_session/',
        'tmp/flask_session/',
        os.path.join(os.path.expanduser('~'), '.cache', 'flask_session'),
        '/tmp/flask_session/'
    ]
    
    cleared_count = 0
    
    for path in session_paths:
        if os.path.exists(path):
            try:
                session_files = glob.glob(os.path.join(path, '*'))
                for file in session_files:
                    if os.path.isfile(file):
                        os.remove(file)
                        cleared_count += 1
                        print(f"Removed session file: {file}")
                if session_files:
                    print(f"Cleared {len(session_files)} session files from {path}")
            except Exception as e:
                print(f"Error clearing sessions from {path}: {e}")
    
    if cleared_count == 0:
        print("No Flask session files found to clear.")
    else:
        print(f"Total session files cleared: {cleared_count}")

if __name__ == "__main__":
    print("VaaniMitra Session Cleanup")
    print("=" * 30)
    clear_flask_sessions()
    print("\nSession cleanup completed!")
    print("Please restart your browser and clear cookies for localhost:5000")
