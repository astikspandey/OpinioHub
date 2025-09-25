#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

# Check if virtual environment exists, if not, create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip
# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:3000

deactivate