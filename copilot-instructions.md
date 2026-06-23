# GitHub Copilot CLI & Agent Coding Instructions

This file guides AI agents when developing or modifying this repository.

## Developer Guidelines

- **Port Configuration**: Always run and refer to the development server on port `8010` (e.g., `python manage.py runserver 127.0.0.1:8010`).
- **Python Setup**: Standard environment uses a virtual environment under `.venv`. Prefer `uv pip install` over standard `pip install` for installing dependencies if `uv` is available.
- **Frontend Changes**:
  - CSS is built with Tailwind CSS v4.0.
  - Do NOT modify CSS directly under `website/static/css/site.css`. Modify `website/static_src/styles.css` and compile using `npm run build` or run `npm run dev` to watch changes.
  - Custom JavaScript should either be implemented inline with Alpine.js or added to `website/static/js/` and referenced.
- **Animations & Icons**:
  - Use `motion` for fluid animations.
  - Use `lucide` for SVG icons. Remember to initialize icons in `base.html` or other templates' `extra_js` block.
- **Tests**:
  - Always run `pytest` after making code changes.
  - Ensure any new features have corresponding tests in `tests/`.
- **Linting**:
  - Format python files using `ruff format .` and check with `ruff check .`.
  - Format HTML files with `djlint website/templates --reformat`.
