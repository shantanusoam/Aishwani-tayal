# Active Tasks & Implementation Notes

## Completed Initial Bootstrap
- [x] Initialized project structure and directory layout
- [x] Set up Python 3.12 virtual environment and dependencies
- [x] Configured Django settings to use `django-environ` and `WhiteNoise`
- [x] Set default port configuration to `8010`
- [x] Implemented Tailwind CSS v4.0 with automated compiler assets
- [x] Created `base.html` and `home.html` utilizing Alpine.js, Lucide Icons, and Motion animations
- [x] Added automated local and remote `scripts/deploy.sh` script
- [x] Wrote Django unit and integration tests under `tests/`
- [x] Tested and confirmed successful `collectstatic` post-processing and passing `pytest` test runs

## Discovered During Work
- [x] Home awards section auto-scroll like About Us certifications (2026-08-11)
- [x] Fix services section duplicate cards on edit/delete (2026-07-03): removed duplicate template loop and stopped `_seed_home_services_content()` from re-seeding on every request.
- [x] Integrate TinyMCE rich text editor for CMS fields in Django admin (2026-07-03).
- [x] Final touches (2026-07-04): WhatsApp/phone/address update, hero CTA to contact form, WhatsApp/FB social icons, awards one-row layout, stats scroll count-up, services card Playfair font, CCTS before Workshops in nav.
- [ ] Implement additional page views (About, Services, Contact)
- [ ] Connect custom contact form and database model (if needed)
- [ ] Configure production server environment and systemd/Nginx configurations
