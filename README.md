# Kitaab - Digital Library Management System

Kitaab is a comprehensive digital library management system designed to streamline book management, issuance, and access control. The application allows librarians to manage book collections and users to browse, request, and read books online.

## Features

- **User Authentication**: Separate login systems for users and librarians
- **Book Management**: Add, edit, delete, and categorize books by sections
- **Book Issuance**: Request, approve, deny, and track book issuances
- **Digital Reading**: Read books online in PDF format
- **Dashboard**: Analytics and management tools for librarians
- **Responsive UI**: Built with Vue 3 for a smooth user experience

## Architecture

Kitaab uses a modern client-server architecture:
- **Frontend**: Vue 3 with Vite build tool
- **Backend**: Python Flask API server with SQLite database
- **Authentication**: JWT-based authentication system

## Project Setup

### Frontend Setup

```sh
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Create a .env file with backend URL (example)
echo "VITE_BACKEND_URL=http://localhost:5000" > .env

# Compile and hot-reload for development
npm run dev

# Compile and minify for production
npm run build
```

### Backend Setup

```sh
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
flask run
```

### Frontend Structure

- `src/components` - Vue components
- `src/views` - Page views
- `src/services` - API connectors and operations
- `src/router` - Route definitions
- `src/assets` - Static assets including images and styles

### Backend Structure

- `models` - Database models
- `routes` - API endpoints
- `instance` - Database instance folder
- `app.py` - Main application entry point

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).
