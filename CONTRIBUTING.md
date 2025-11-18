# Contributing Guide

Thank you for your interest in contributing to the Contextual Ad Copy Micro-Engine! This document provides guidelines for development and contribution.

## Development Setup

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL 14+
- Git

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/contextual-ad-engine.git
   cd contextual-ad-engine
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your local credentials
   ```

3. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb contextual_engine
   
   # Run migrations
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```

4. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   cp .env.example .env.local
   # Edit .env.local with your local API URL
   ```

5. **Run Development Servers**
   
   Terminal 1 (Backend):
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```
   
   Terminal 2 (Frontend):
   ```bash
   cd frontend
   npm run dev
   ```

6. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where applicable
- Maximum line length: 120 characters
- Use docstrings for functions and classes

**Linting**
```bash
cd backend
flake8 app/ --max-line-length=120
```

### TypeScript (Frontend)

- Follow ESLint rules
- Use TypeScript strict mode
- Prefer functional components with hooks
- Use Tailwind CSS for styling

**Linting**
```bash
cd frontend
npm run lint
```

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ --cov=app --cov-report=term-missing
```

**Writing Tests**
- Place tests in `backend/tests/`
- Name test files `test_*.py`
- Use fixtures for common setup
- Aim for 80%+ code coverage

### Frontend Tests

```bash
cd frontend
npm run test
```

## Git Workflow

### Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Hotfix: `hotfix/description`
- Documentation: `docs/description`

### Commit Messages

Follow conventional commits format:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(backend): add rate limiting to generation endpoint
fix(frontend): resolve dashboard loading state
docs(readme): update installation instructions
```

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Write/update tests
4. Run linting and tests locally
5. Commit with clear messages
6. Push to your fork
7. Create a pull request with:
   - Clear title and description
   - Reference to related issues
   - Screenshots (if UI changes)
   - Test results

## Project Structure

```
contextual-ad-engine/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── alembic/          # Database migrations
│   ├── tests/            # Backend tests
│   └── main.py           # Application entry point
├── frontend/
│   ├── app/              # Next.js app directory
│   ├── components/       # React components
│   ├── hooks/            # Custom hooks
│   └── lib/              # Utilities and API client
└── .github/
    └── workflows/        # CI/CD pipelines
```

## Adding New Features

### Backend API Endpoint

1. Create schema in `app/schemas/schemas.py`
2. Add endpoint in appropriate router (`app/api/`)
3. Implement business logic in `app/services/`
4. Write tests in `tests/`
5. Update API documentation

### Frontend Component

1. Create component in `components/`
2. Add types if needed
3. Integrate with API using `lib/api.ts`
4. Add to appropriate page in `app/`
5. Style with Tailwind CSS

### Database Changes

1. Modify model in `app/models/`
2. Generate migration:
   ```bash
   alembic revision --autogenerate -m "description"
   ```
3. Review generated migration
4. Apply migration:
   ```bash
   alembic upgrade head
   ```

## Common Tasks

### Adding a New API Dependency

```bash
cd backend
pip install package-name
pip freeze > requirements.txt
```

### Adding a New Frontend Dependency

```bash
cd frontend
npm install package-name
```

### Updating Environment Variables

1. Update `.env.example` files
2. Update documentation
3. Notify team members
4. Update deployment configs

## Debugging

### Backend Debugging

Use Python debugger:
```python
import pdb; pdb.set_trace()
```

Or use logging:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")
```

### Frontend Debugging

Use browser DevTools and console.log:
```typescript
console.log('Debug:', variable)
```

## Performance Guidelines

### Backend

- Use async/await for I/O operations
- Implement database query optimization
- Add indexes for frequently queried fields
- Cache expensive operations

### Frontend

- Minimize API calls
- Use React.memo for expensive components
- Implement proper loading states
- Optimize images and assets

## Security Best Practices

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Sanitize data before database operations
- Use parameterized queries
- Implement proper authentication checks
- Keep dependencies updated

## Documentation

- Update README.md for user-facing changes
- Update DEPLOYMENT.md for infrastructure changes
- Add inline comments for complex logic
- Update API documentation in FastAPI
- Keep CONTRIBUTING.md current

## Questions?

If you have questions or need help:
1. Check existing documentation
2. Search closed issues
3. Ask in pull request comments
4. Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
