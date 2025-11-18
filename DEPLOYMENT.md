# Deployment Guide

This document provides step-by-step instructions for deploying the Contextual Ad Copy Micro-Engine to production.

## Prerequisites

Before deploying, ensure you have:

1. **GitHub Account** - For code hosting and CI/CD
2. **Render Account** - For backend hosting
3. **Vercel Account** - For frontend hosting
4. **Google AI Studio API Key** - For Gemini AI access
5. **Stripe Account** - For payment processing
6. **PostgreSQL Database** - Provided by Render

## Backend Deployment (Render)

### Step 1: Create PostgreSQL Database

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `contextual-engine-db`
   - Database: `contextual_engine`
   - User: (auto-generated)
   - Region: Oregon (or nearest)
   - Plan: Starter ($7/month)
4. Click "Create Database"
5. Copy the **Internal Database URL** for later use

### Step 2: Create Web Service

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `contextual-engine-api`
   - Region: Oregon
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `DATABASE_URL`: (Paste Internal Database URL from Step 1)
   - `GEMINI_API_KEY`: (Your Google AI Studio API key)
   - `JWT_SECRET`: (Generate a random 256-bit string)
   - `STRIPE_SECRET_KEY`: (Your Stripe secret key)
   - `STRIPE_WEBHOOK_SECRET`: (Your Stripe webhook secret)
   - `CORS_ORIGINS`: `https://your-app.vercel.app`
   - `SENTRY_DSN`: (Optional - for error tracking)
5. Click "Create Web Service"

### Step 3: Run Database Migrations

1. Wait for the service to deploy
2. In Render Dashboard, go to your web service
3. Click "Shell" tab
4. Run:
   ```bash
   cd backend
   alembic revision --autogenerate -m "initial"
   alembic upgrade head
   ```

### Step 4: Configure Stripe Webhook

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/webhooks)
2. Click "Add endpoint"
3. Endpoint URL: `https://your-render-app.onrender.com/api/v1/webhooks/stripe`
4. Events to send:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the **Signing secret** and update `STRIPE_WEBHOOK_SECRET` in Render

## Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. Log in to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Add Environment Variables:
   - `NEXT_PUBLIC_API_URL`: `https://your-render-app.onrender.com`
   - `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: (Your Stripe publishable key)
6. Click "Deploy"

### Step 2: Configure Custom Domain (Optional)

1. In Vercel project settings, go to "Domains"
2. Add your custom domain
3. Update DNS records as instructed
4. Update `CORS_ORIGINS` in Render to include your custom domain

## GitHub Actions CI/CD

### Step 1: Add GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add the following secrets:
   - `RENDER_SERVICE_ID`: (From Render service settings)
   - `RENDER_API_KEY`: (From Render account settings)
   - `VERCEL_TOKEN`: (From Vercel account settings)
   - `VERCEL_ORG_ID`: (From Vercel project settings)
   - `VERCEL_PROJECT_ID`: (From Vercel project settings)

### Step 2: Verify CI/CD Pipeline

1. Push a commit to the `main` branch
2. Go to Actions tab in GitHub
3. Verify that the workflow runs successfully
4. Check that both backend and frontend are deployed

## Post-Deployment Verification

### Health Check

1. Visit: `https://your-render-app.onrender.com/api/v1/health`
2. Should return: `{"status": "ok", "version": "1.0.0"}`

### Frontend Check

1. Visit: `https://your-app.vercel.app`
2. Should redirect to login page
3. Create a test account
4. Verify dashboard loads correctly

### End-to-End Test

1. Sign up for a new account
2. Generate ad copy with a test URL
3. Verify variations are displayed
4. Check usage counter updates
5. Test Stripe subscription flow (use test mode)

## Monitoring & Maintenance

### Logs

**Backend Logs (Render)**
- Go to Render Dashboard → Your service → Logs tab
- Monitor for errors and performance issues

**Frontend Logs (Vercel)**
- Go to Vercel Dashboard → Your project → Deployments
- Click on a deployment → View Function Logs

### Database Backups

Render automatically backs up PostgreSQL databases daily. To restore:
1. Go to Render Dashboard → Your database
2. Click "Backups" tab
3. Select a backup and click "Restore"

### Scaling

**Backend (Render)**
- Upgrade plan for more resources
- Enable auto-scaling in service settings

**Frontend (Vercel)**
- Automatically scales with traffic
- Monitor usage in Vercel Dashboard

### Error Tracking (Sentry)

If you configured Sentry:
1. Go to [Sentry Dashboard](https://sentry.io/)
2. Monitor errors and performance
3. Set up alerts for critical issues

## Rollback Procedure

### Backend Rollback

1. Go to Render Dashboard → Your service → Events
2. Find the last successful deployment
3. Click "Redeploy"

### Frontend Rollback

1. Go to Vercel Dashboard → Your project → Deployments
2. Find the last working deployment
3. Click "..." → "Promote to Production"

## Troubleshooting

### Backend Issues

**Database Connection Errors**
- Verify `DATABASE_URL` is correct
- Check database is running in Render
- Ensure migrations are up to date

**AI Generation Failures**
- Verify `GEMINI_API_KEY` is valid
- Check API quota in Google AI Studio
- Review error logs in Render

**Stripe Webhook Failures**
- Verify webhook URL is correct
- Check `STRIPE_WEBHOOK_SECRET` matches Stripe
- Test webhook in Stripe Dashboard

### Frontend Issues

**API Connection Errors**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running

**Authentication Issues**
- Clear browser localStorage
- Check JWT token expiration
- Verify backend `/auth` endpoints work

## Security Checklist

- [ ] All environment variables are set correctly
- [ ] JWT secret is strong and unique
- [ ] Stripe keys are in test mode initially
- [ ] CORS origins are restricted to your domains
- [ ] Database credentials are secure
- [ ] HTTPS is enabled on all services
- [ ] Webhook signatures are verified
- [ ] Rate limiting is configured (future enhancement)

## Performance Optimization

### Backend

- Enable connection pooling (already configured)
- Monitor slow queries in PostgreSQL
- Consider adding Redis for caching (V2)
- Optimize AI prompts for faster responses

### Frontend

- Images are optimized (Next.js automatic)
- Code splitting enabled (Next.js automatic)
- Monitor Core Web Vitals in Vercel
- Consider adding CDN for static assets

## Cost Estimation

**Monthly Costs (Estimated)**

- Render PostgreSQL Starter: $7
- Render Web Service (Starter): $7
- Vercel (Hobby): Free (or $20 for Pro)
- Google AI Studio: Pay-per-use (~$0.10-1.00 per 1000 requests)
- Stripe: 2.9% + $0.30 per transaction
- Sentry (Optional): Free tier available

**Total**: ~$14-34/month + usage-based costs

## Support

For deployment issues:
- Backend: Check Render documentation
- Frontend: Check Vercel documentation
- CI/CD: Check GitHub Actions logs
- General: Review application logs and error messages
