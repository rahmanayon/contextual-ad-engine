# Contextual Ad Copy Micro-Engine

An AI-powered web application that generates contextual ad copy variations by scraping website content and using advanced language models.

## Overview

The Contextual Ad Copy Micro-Engine is designed for media planners and marketers who need to quickly generate multiple ad copy variations based on landing page content. The system scrapes a target URL, extracts key information, and uses AI to generate tailored ad copy with different strategies and tones.

## Architecture

The application follows a modern full-stack architecture with clear separation of concerns.

### Technology Stack

**Frontend**
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- React hooks for state management

**Backend**
- Python 3.11+ with FastAPI
- PostgreSQL for data persistence
- Alembic for database migrations
- SQLAlchemy ORM

**AI & Scraping**
- Google Gemini API (gemini-2.5-flash-lite-preview-04-17)
- BeautifulSoup4 for web scraping
- Async/await for non-blocking operations

**Authentication & Payments**
- JWT-based authentication
- Stripe for subscription management
- Secure password hashing with bcrypt

**Deployment**
- Frontend: Vercel
- Backend: Render
- Database: Render PostgreSQL
- CI/CD: GitHub Actions

## Features

### MVP Features
- User authentication (signup/login)
- Single-page generator dashboard
- URL scraping and content extraction
- AI-powered ad copy generation
- Stripe subscription integration
- Usage tracking (500 generations/month for Pro plan)
- Responsive design

### Explicitly Out of Scope (V1)
- Team accounts
- API access
- Browser extension
- Project saving/history
- Analytics dashboard
- Image/video analysis
- Complex JavaScript-heavy site scraping
- Direct ad platform integration

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.11+
- PostgreSQL 14+
- Stripe account
- Google AI Studio API key

### Local Development

**Backend Setup**
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
alembic revision --autogenerate -m "initial"
alembic upgrade head
uvicorn main:app --reload
```

**Frontend Setup**
```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your API URL
npm run dev
```

Visit http://localhost:3000 to access the application.

### Environment Variables

**Backend (.env)**
- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY`: Google AI Studio API key
- `GEMINI_MODEL`: Model version (gemini-2.5-flash-lite-preview-04-17)
- `JWT_SECRET`: Secret for JWT token signing
- `STRIPE_SECRET_KEY`: Stripe secret key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook secret
- `SENTRY_DSN`: (Optional) Sentry error tracking

**Frontend (.env.local)**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Stripe publishable key

## Deployment

### GitHub Secrets Required
- `RENDER_SERVICE_ID`
- `RENDER_API_KEY`
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `GEMINI_API_KEY` (also add to Render dashboard)

### Deployment Steps
1. Push code to GitHub main branch
2. GitHub Actions automatically triggers CI/CD
3. Backend deploys to Render
4. Frontend deploys to Vercel
5. Run database migrations on Render
6. Monitor deployment logs

First successful deployment should return 200 OK at: `https://your-app.vercel.app/api/v1/health`

## API Documentation

### Authentication Endpoints
- `POST /api/v1/auth/signup` - Create new user account
- `POST /api/v1/auth/login` - Authenticate user

### Generation Endpoints
- `POST /api/v1/generate` - Generate ad copy variations
- `GET /api/v1/health` - Health check endpoint

### User Endpoints
- `GET /api/v1/user/me` - Get current user profile
- `GET /api/v1/user/usage` - Get usage statistics

## Testing

**Backend Tests**
```bash
cd backend
pytest tests/ --cov=app --cov-report=term-missing
```

**Frontend Tests**
```bash
cd frontend
npm run test
npm run lint
```

## Success Metrics

The MVP targets the following key performance indicators:

- **Activation Rate**: % of signups who complete first generation
- **Paid Conversion Rate**: % of free users who upgrade to Pro
- **Generations per Session**: Target 5+ (indicates product-market fit)
- **Qualitative Feedback**: 1-5 star rating system

## Project Structure

```
contextual-ad-engine/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── alembic/
│   ├── tests/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   └── package.json
├── .github/
│   └── workflows/
└── README.md
```

## Contributing

This is a private MVP project. For questions or issues, contact the development team.

## License

Proprietary - All rights reserved.
