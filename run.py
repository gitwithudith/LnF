#!/usr/bin/env python3
"""
Main entry point for the Campus Lost & Found Flask application
Run this file to start the development server
"""
import os
from app import create_app

# Create the Flask application
app = create_app('development')

if __name__ == '__main__':
    # Get port from environment variable or use 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the development server
    # debug=True enables auto-reload and better error messages
    app.run(
        host='0.0.0.0',  # Makes server accessible from network
        port=port,
        debug=True
    )
