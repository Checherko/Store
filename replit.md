# Megano E-Commerce Frontend

## Overview
This is a Django-based e-commerce frontend template (Megano). It provides the UI for an online store and expects a backend API to be implemented separately.

## Project Structure
- `megano/` - Django project settings and configuration
- `diploma-frontend/` - Frontend Django app package containing:
  - Templates (HTML pages)
  - Static assets (CSS, JS, images, fonts)
  - URL routing for frontend pages

## Current State
- Frontend template is fully functional and displays properly
- The frontend expects API endpoints to be implemented (see `/diploma-frontend/swagger/swagger.yaml` for API contract)
- API 404 errors are expected until backend is implemented

## Running the Project
The Django development server runs on port 5000:
```bash
python manage.py runserver 0.0.0.0:5000
```

## Configuration
- `ALLOWED_HOSTS = ['*']` - Allows all hosts for development
- `CSRF_TRUSTED_ORIGINS` - Configured for Replit domains
- `X_FRAME_OPTIONS = 'ALLOWALL'` - Allows iframe embedding

## API Contract
The frontend expects these API endpoints (see swagger.yaml for details):
- `/api/banners` - Home page banners
- `/api/categories` - Product categories
- `/api/products/popular` - Popular products
- `/api/products/limited` - Limited edition products
- `/api/basket` - Shopping cart

## Dependencies
- Django 5.2.9
- Python 3.11

## Recent Changes
- 2025-12-25: Initial import and setup for Replit environment
