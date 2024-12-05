#!/bin/bash

echo "Starting setup for Python, Node.js, and Create React App on Windows"

# Function to prompt user for yes/no response
prompt_user() {
    while true; do
        read -p "$1 (yes/no): " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Check and Install Python
if command -v python &> /dev/null; then
    echo "Python is already installed."
    python --version
else
    if prompt_user "Python is not installed. Do you want to install Python?"; then
        echo "Installing Python..."
        powershell -Command "& {Start-Process 'https://www.python.org/ftp/python/3.11.6/python-3.11.6-amd64.exe' -Wait}"
        echo "Ensure to check 'Add Python to PATH' during the installation."
        if command -v python &> /dev/null; then
            echo "Python installed successfully."
            python --version
        else
            echo "Python installation failed. Please check your setup and retry."
            exit 1
        fi
    else
        echo "Skipping Python installation."
    fi
fi

# Check and Install Node.js
if command -v node &> /dev/null; then
    echo "Node.js is already installed."
    node --version
    echo "npm version:"
    npm --version
else
    if prompt_user "Node.js is not installed. Do you want to install Node.js?"; then
        echo "Installing Node.js..."
        powershell -Command "& {Start-Process 'https://nodejs.org/dist/v18.17.0/node-v18.17.0-x64.msi' -Wait}"
        if command -v node &> /dev/null; then
            echo "Node.js installed successfully."
            node --version
            echo "npm version:"
            npm --version
        else
            echo "Node.js installation failed. Please check your setup and retry."
            exit 1
        fi
    else
        echo "Skipping Node.js installation."
    fi
fi

# Check and Install Create React App
if command -v create-react-app &> /dev/null; then
    echo "Create React App is already installed."
    create-react-app --version
else
    if prompt_user "Create React App is not installed globally. Do you want to install it?"; then
        echo "Installing Create React App globally..."
        npm install -g create-react-app
        if command -v create-react-app &> /dev/null; then
            echo "Create React App installed successfully."
            create-react-app --version
        else
            echo "Failed to install Create React App. Please check your npm configuration."
            exit 1
        fi
    else
        echo "Skipping Create React App installation."
    fi
fi

## Clone Repository
#if prompt_user "Do you want to clone a repository?"; then
#    echo "Cloning the repository..."
#    echo "Enter the repository URL:"
#    read REPO_URL
#    git clone "$REPO_URL"
#
#    echo "Enter the directory name where the repository was cloned:"
#    read REPO_DIR
#    cd "$REPO_DIR" || exit 1
#else
#    echo "Skipping repository cloning."
#fi

# Set up Backend
if [ -d "backend" ]; then
    if prompt_user "Do you want to set up the backend?"; then
        echo "Setting up the backend..."
        #cd backend || exit 1
        if [ ! -d "venv" ]; then
            python -m venv venv
        fi
        source venv/Scripts/activate
        pip install -r requirements.txt
        echo "Backend setup complete."
        #cd ..
    else
        echo "Skipping backend setup."
    fi
else
    echo "Backend directory not found. Skipping backend setup."
fi

# Set up Frontend
if [ -d "front-end" ]; then
    if prompt_user "Do you want to set up the frontend?"; then
        echo "Setting up the frontend..."
        cd front-end || exit 1
        if [ ! -f package.json ]; then
            echo "Initializing a new React app..."
            npx create-react-app .
        fi
        npm install
        echo "Frontend setup complete."
        cd ..
    else
        echo "Skipping frontend setup."
    fi
else
    echo "Frontend directory not found. Skipping frontend setup."
fi

