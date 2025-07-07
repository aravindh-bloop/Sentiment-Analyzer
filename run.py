#!/usr/bin/env python3
"""
Sentiment Analysis Tool - Standalone Runner
This script allows you to run the sentiment analysis tool easily
"""

import os
import sys
import logging
from main import app

def main():
    """Run the Flask application"""
    print("=" * 60)
    print("   🧠 SENTIMENT ANALYSIS TOOL")
    print("=" * 60)
    print("Starting the application...")
    print(f"Access the tool at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Configure Flask app
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    
    # Run the application
    try:
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=True
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("   👋 Thank you for using Sentiment Analysis Tool!")
        print("=" * 60)
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()