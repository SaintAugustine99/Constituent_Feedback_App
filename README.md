# Jamii Platform

A full-stack civic engagement platform for Kenyan citizens to participate in governance, track legislation, report issues, and interact with their elected representatives.

## Overview

Jamii (Swahili for "community") bridges the gap between citizens and government by providing digital tools for public participation — a right guaranteed under Article 10 and Article 196 of the Constitution of Kenya 2010.

## Architecture

| Layer | Stack |
|-------|-------|
| **Backend** | Django 4.2 + Django REST Framework, SQLite/PostgreSQL |
| **Frontend** | React 19 + Vite, styled-components, Framer Motion |
| **Auth** | Token-based (DRF TokenAuthentication) |
| **AI** | Gemini Pro via google-generativeai |
| **Deploy** | Fly.io (backend), Vercel (frontend) |

## Features

### Legislative Tracker
Browse active bills and policies, view feedback statistics (support/oppose/amend), and submit public feedback — as a registered citizen or as a guest. Each instrument tracks its docket, category, status, and participation deadline.

### AI Civic Assistant
Context-aware chat powered by Gemini Pro. Available as a floating widget on every page and as a dedicated full-page experience at `/assistant`. The assistant knows about active legislation, current feedback sentiment, and the user's location — enriching every response with relevant civic context.

### Service Request Reporting
Authenticated citizens can report infrastructure issues (roads, water, power, security, environment) with descriptions, location data, and photo evidence.

### Facility Booking
Browse public facilities (halls, fields, parks) and book time slots. Built-in overlap detection prevents double-bookings.

### Project Tracker & Citizen Audit
Track government projects by ward — budget allocated vs. spent, completion percentage, contractor details. Citizens can post audit updates with photos to hold contractors accountable.

### Know Your Leaders
Directory of elected officials (MCAs, MPs, Governors, Senators, Women Reps) filterable by ward, constituency, and county. Includes contact information.

### News & Government Resources
Curated links to Kenya Law, Parliament, IEBC, and other resources. News feed with articles from relevant sources.

## Project Structure

```
jamii-platform/
├── backend/
│   ├── core/              # Django settings, root URLs
│   ├── accounts/          # User model (extends AbstractUser with ward FK)
│   ├── locations/         # County → Constituency → Ward hierarchy + Officials
│   ├── legislative_tracker/  # Bills, feedback, dockets, status reports
│   ├── issues/            # Service request reporting
│   ├── facilities/        # Facility listing and booking with overlap validation
│   ├── projects/          # Project tracking and citizen audit updates
│   ├── news/              # News articles and government resources
│   ├── assistant/         # AI assistant (Gemini Pro integration)
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/    # Header, DashboardLayout, ChatWidget, forms
│   │   ├── pages/         # LegislationPage, AssistantPage, IssuesPage, etc.
│   │   ├── context/       # AuthContext, AssistantContext
│   │   ├── services/      # Axios API service layer
│   │   ├── hooks/         # useLegislation custom hook
│   │   └── styles/        # Theme (light/dark) and global styles
│   └── package.json
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env      # configure SECRET_KEY, GEMINI_API_KEY, etc.
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL` in a `.env` file if the backend isn't at `http://127.0.0.1:8000/api`.

### Running Tests

```bash
cd backend
python manage.py test
```

## API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/register/` | POST | Public | User registration |
| `/api/login/` | POST | Public | Token login |
| `/api/counties/` | GET | Public | List counties |
| `/api/constituencies/` | GET | Public | Filter by county_id |
| `/api/wards/` | GET | Public | Filter by constituency_id |
| `/api/legislation/instruments/` | GET | Public | List all instruments |
| `/api/legislation/instruments/active/` | GET | Public | Only open-for-participation |
| `/api/legislation/instruments/{id}/stats/` | GET | Public | Feedback statistics |
| `/api/legislation/feedback/` | POST | Public | Submit feedback (guest or auth) |
| `/api/issues/requests/` | GET/POST | Auth | Service requests (own only) |
| `/api/facilities/list/` | GET | Public | List facilities |
| `/api/facilities/bookings/` | GET/POST | Auth | Bookings (own only) |
| `/api/projects/` | GET | Public | List projects |
| `/api/projects/updates/` | GET/POST | Read: Public, Write: Auth | Citizen audit updates |
| `/api/locations/officials/` | GET | Public | Officials directory |
| `/api/news/articles/` | GET | Public | News articles |
| `/api/news/resources/` | GET | Public | Government resources |
| `/api/assistant/chat/` | POST | Public | AI assistant chat |

## Future Enhancements

- **Real-time notifications** — WebSocket alerts when bills near deadline or issues change status
- **SMS integration** — Africa's Talking API for citizens without reliable internet
- **Offline support** — PWA with service worker for rural areas with poor connectivity
- **Analytics dashboard** — Visual breakdown of feedback by ward/constituency/county for officials
- **Multi-language** — Swahili and other local language support
- **Document generation** — Auto-generate PDF memoranda from structured feedback
- **Geospatial mapping** — Map view for service issues and project locations
- **Accessibility audit** — WCAG 2.1 compliance for screen readers and assistive devices
- **Rate limiting and abuse prevention** — Throttle API endpoints, CAPTCHA on public forms
- **Email verification** — Confirm user email during registration
- **Role-based access** — Official/admin dashboards with moderation capabilities
- **Mobile app** — React Native wrapper for Android (Kenya's dominant platform)
