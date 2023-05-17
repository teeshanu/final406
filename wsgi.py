import sys
import os

# Add the path to your Flask app
sys.path.insert(0, '/Users/teeshanu/Desktop/final406')

# Set the environment variable to point to your Flask app
os.environ['FLASK_APP'] = 'app.py'

from app import app as application
