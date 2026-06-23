# Aishwani Tayal Website

A modern, fast, and gorgeous Django + Tailwind CSS starter project.

## Technology Stack

- **Python 3.12** & **Django 5.2**
- **Tailwind CSS v4.0** (via `@tailwindcss/cli`)
- **Alpine.js** for lightweight client-side interactivity
- **Motion** for butter-smooth ES-module-based animations
- **Lucide** for SVG icons
- **WhiteNoise** with compressed and manifest-hashed static files serving
- **Pytest** for clean testing
- **Ruff** + **djLint** + **pre-commit** for code quality

## Local Development Setup

To bring a fresh clone up locally, run:

```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies (Python & Node)
uv pip install -r requirements.txt  # Or pip install -r requirements.txt
npm install

# 3. Create .env file from template
cp .env.example .env

# 4. Compile frontend assets
npm run build

# 5. Run migrations
python manage.py migrate

# 6. Start development server (runs on port 8010 as requested)
python manage.py runserver 127.0.0.1:8010
```

For live CSS development, run this in a second terminal to watch and rebuild:

```bash
npm run dev
```

## Running Tests and Lints

Validate the codebase using:

```bash
# Run test suite
pytest

# Check & format Python files
ruff check .
ruff format .

# Reformat HTML templates
djlint website/templates --reformat
```

## Deployment

Deploy using the automated script:

```bash
# Local/dry-run checks
scripts/deploy.sh

# Run remote deployment (with SSH/rsync configuration)
REMOTE_HOST=your-server-ip PORT=8010 SERVER_NAME=aishwanitayal.com scripts/deploy.sh
```
