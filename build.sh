#!/usr/bin/env bash
# exit on error
set -o errexit

# Install specific Python version
pyenv install 3.10.0
pyenv global 3.10.0

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --no-input
