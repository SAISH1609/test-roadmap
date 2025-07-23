# Railway Deployment Guide

## Pre-deployment Checklist

### 1. Code Changes Made
- ✅ Added Railway configuration files
- ✅ Updated CORS settings for Railway domains
- ✅ Created database seeding script
- ✅ Updated frontend build configuration
- ✅ Added Procfiles for both frontend and backend

### 2. Files Added/Modified
```
📁 Backend Changes:
- backend/Procfile (new)
- backend/nixpacks.toml (new) 
- backend/railway_seed.py (new)
- backend/start.sh (new)
- backend/main.py (modified - CORS & port)

📁 Frontend Changes:
- frontend/Procfile (new)
- frontend/nixpacks.toml (new)
- frontend/package.json (modified - scripts)
- frontend/vite.config.ts (modified - port config)

📁 Root Changes:
- railway.json (new)
```

## Deployment Steps

### Phase 1: Repository Setup
1. Push all changes to your GitHub repository
2. Ensure your repository is public or Railway has access

### Phase 2: Railway Project Creation

#### Step 1: Create New Project
1. Go to Railway dashboard
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `test-roadmap` repository

#### Step 2: Configure Services
Railway will detect multiple services. You need to deploy them in this order:

### Service 1: Database (PostgreSQL)
1. In Railway dashboard, click "Add Service"
2. Select "Database" → "PostgreSQL"
3. This will create a PostgreSQL instance
4. Note down the connection variables (Railway provides these automatically)

### Service 2: Backend (FastAPI)
1. Click "Add Service" → "GitHub Repository"
2. Select your repository
3. Set the following configurations:
   - **Root Directory**: `backend`
   - **Build Command**: (leave empty - nixpacks will handle)
   - **Start Command**: (leave empty - nixpacks will handle)

#### Environment Variables for Backend:
Add these in Railway dashboard under Backend service → Variables:
```bash
DATABASE_URL=postgresql://postgres:password@host:port/database
# Railway will auto-generate this, just reference the PostgreSQL service
```

**Important**: Use Railway's variable referencing:
- Click "Add Variable"
- Select "Reference" instead of "Raw"
- Reference the PostgreSQL service's DATABASE_URL

### Service 3: Frontend (React)
1. Click "Add Service" → "GitHub Repository"  
2. Select your repository again
3. Set configurations:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Start Command**: `npm run preview`

#### Environment Variables for Frontend:
```bash
VITE_API_URL=https://your-backend-service.railway.app/api
```

**Note**: Replace `your-backend-service` with your actual backend service URL from Railway.

### Phase 3: Deployment Process

#### Step 1: Deploy Database
1. Database deploys automatically
2. Wait for it to be "Active"
3. Copy the connection string for reference

#### Step 2: Deploy Backend
1. Backend will build and deploy
2. Railway will run the seeding script automatically
3. Check logs to ensure database seeding completed
4. Copy the backend URL (something like: https://backend-production-xxxx.up.railway.app)

#### Step 3: Deploy Frontend
1. Update frontend environment variable with backend URL
2. Redeploy frontend service
3. Frontend should now be accessible

### Phase 4: Post-Deployment Configuration

#### Update CORS (if needed)
If you encounter CORS issues:
1. Go to backend service
2. Update the `main.py` CORS settings to include your specific Railway domain
3. Redeploy backend

#### Database Management
- Use Railway's database dashboard to view data
- Connect using the provided connection string for external tools

### Phase 5: Testing

#### Test Backend API
Visit: `https://your-backend-url.railway.app/health`
Should return: `{"status": "healthy", "message": "API is running", "cors": "enabled"}`

#### Test Frontend
Visit: `https://your-frontend-url.railway.app`
Should load your React application

#### Test Integration
Ensure frontend can communicate with backend APIs.

## Common Issues & Solutions

### Issue 1: Database Connection Timeout
**Solution**: Ensure DATABASE_URL is correctly referenced from the PostgreSQL service.

### Issue 2: Frontend Can't Reach Backend
**Solution**: 
1. Check VITE_API_URL environment variable
2. Verify CORS settings in backend
3. Ensure both services are deployed and active

### Issue 3: Build Failures
**Solution**:
1. Check build logs in Railway dashboard
2. Verify all dependencies are in requirements.txt/package.json
3. Ensure nixpacks.toml configurations are correct

### Issue 4: Database Not Seeded
**Solution**:
1. Check backend deployment logs
2. Manually run seeding script if needed
3. Connect to database and verify tables exist

## Monitoring & Maintenance

### Logs
- Access logs through Railway dashboard
- Monitor both frontend and backend services
- Set up alerts for service failures

### Updates
- Push changes to GitHub repository
- Railway will auto-deploy on push (if enabled)
- Monitor deployment status in dashboard

### Scaling
- Railway automatically handles scaling
- Monitor resource usage in dashboard
- Upgrade plan if needed for higher usage

## Environment Variables Summary

### Backend Service:
```bash
DATABASE_URL=postgresql://user:pass@host:port/db  # Reference from PostgreSQL service
```

### Frontend Service:
```bash
VITE_API_URL=https://your-backend-service.railway.app/api
```

## Next Steps After Deployment

1. **Custom Domain**: Set up custom domain in Railway dashboard
2. **SSL**: Railway provides SSL automatically
3. **Monitoring**: Set up monitoring and alerts
4. **Backup**: Configure database backups
5. **CI/CD**: Set up automatic deployments from GitHub

## Support Resources

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Your deployment URLs will be available in Railway dashboard
