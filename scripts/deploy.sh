#!/bin/bash
# Deployment script for Aishwani Tayal Website
#
# Usage:
#   scripts/deploy.sh
#
# Override defaults by setting environment variables:
#   REMOTE_HOST=example.com SERVER_NAME=app.example.com PORT=8010 scripts/deploy.sh

set -e

# Default configurations
REMOTE_HOST="${REMOTE_HOST:-localhost}"
PORT="${PORT:-8010}"
SERVER_NAME="${SERVER_NAME:-aishwanitayal.local}"
APP_DIR="/var/www/aishwani-tayal"

echo "=========================================================="
echo "Starting deployment sequence for ${SERVER_NAME}..."
echo "Target Host: ${REMOTE_HOST}"
echo "Port: ${PORT}"
echo "=========================================================="

if [ "$REMOTE_HOST" = "localhost" ] || [ "$REMOTE_HOST" = "127.0.0.1" ]; then
    echo "[Local Deploy] Installing Python dependencies..."
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        uv pip install -r requirements.txt || pip install -r requirements.txt
    else
        python3 -m venv .venv
        source .venv/bin/activate
        uv pip install -r requirements.txt || pip install -r requirements.txt
    fi

    echo "[Local Deploy] Installing NPM dependencies and building..."
    npm install
    npm run build

    echo "[Local Deploy] Running Django migrations..."
    python manage.py migrate --noinput

    echo "[Local Deploy] Collecting static files..."
    python manage.py collectstatic --noinput

    echo "[Local Deploy] Completed local deployment checks!"
else
    echo "[Remote Deploy] Preparing files for remote deployment to ${REMOTE_HOST}..."
    # A remote deployment would typically rsync files or run commands via SSH.
    # Below is a standard blueprint for SSH-based remote deployments:
    
    # 1. Sync codebase
    # rsync -avz --exclude-from=.gitignore . user@${REMOTE_HOST}:${APP_DIR}
    
    # 2. Run remote commands
    # ssh user@${REMOTE_HOST} << EOF
    #   cd ${APP_DIR}
    #   python3 -m venv .venv
    #   source .venv/bin/activate
    #   pip install -U pip uv
    #   uv pip install -r requirements.txt
    #   npm install
    #   npm run build
    #   python manage.py migrate --noinput
    #   python manage.py collectstatic --noinput
    #   
    #   # Restart Gunicorn service and reload Nginx
    #   sudo systemctl restart gunicorn-aishwani
    #   sudo systemctl reload nginx
    # EOF
    
    echo "[Remote Deploy] Remote deployment code has been templated."
    echo "[Remote Deploy] Make sure ssh/rsync credentials are set up if utilizing remote features."
fi

echo "=========================================================="
echo "Deployment sequence finished successfully!"
echo "=========================================================="
