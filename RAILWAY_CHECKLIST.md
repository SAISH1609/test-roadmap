# Railway Deployment Checklist

## ✅ Pre-Deployment (Complete these before deploying)

### 1. Repository Preparation
- [ ] All code changes committed and pushed to GitHub
- [ ] Repository is accessible to Railway
- [ ] `.env` files are NOT committed (they're in .gitignore)

### 2. Code Modifications (Already Done)
- [x] Backend CORS updated for Railway domains
- [x] Backend port configuration for Railway
- [x] Frontend build configuration updated
- [x] Database seeding script created
- [x] Health check script created
- [x] Nixpacks configuration files added

## 🚀 Deployment Steps

### Phase 1: Railway Setup
- [ ] 1. Create Railway account at https://railway.app
- [ ] 2. Connect GitHub account to Railway
- [ ] 3. Create new project in Railway
- [ ] 4. Select "Deploy from GitHub repo"
- [ ] 5. Choose your `test-roadmap` repository

### Phase 2: Database Service
- [ ] 1. Add PostgreSQL service to project
- [ ] 2. Wait for database to be active
- [ ] 3. Note the DATABASE_URL (auto-generated)

### Phase 3: Backend Service  
- [ ] 1. Add service from GitHub repo
- [ ] 2. Set root directory to `backend`
- [ ] 3. Add environment variable:
  - [ ] `DATABASE_URL` (reference PostgreSQL service)
- [ ] 4. Deploy and wait for completion
- [ ] 5. Copy backend URL for frontend

### Phase 4: Frontend Service
- [ ] 1. Add service from GitHub repo  
- [ ] 2. Set root directory to `frontend`
- [ ] 3. Add environment variable:
  - [ ] `VITE_API_URL=https://[your-backend-url]/api`
- [ ] 4. Deploy and wait for completion

## 🧪 Testing

### Backend Testing
- [ ] Visit: `https://[backend-url]/health`
- [ ] Should return: `{"status": "healthy", ...}`
- [ ] Check: `https://[backend-url]/api/roadmaps`
- [ ] Should return roadmap data

### Frontend Testing  
- [ ] Visit: `https://[frontend-url]`
- [ ] App should load correctly
- [ ] Test navigation between pages
- [ ] Verify API calls are working

### Integration Testing
- [ ] Frontend can fetch data from backend
- [ ] CORS is working properly
- [ ] Database queries are successful

## 🔧 Troubleshooting

### If Backend Fails to Start:
1. Check Railway logs for backend service
2. Verify DATABASE_URL is correctly set
3. Ensure database service is active
4. Check for any missing environment variables

### If Frontend Can't Reach Backend:
1. Verify VITE_API_URL is correct
2. Check CORS settings in backend
3. Ensure backend service is running
4. Test backend API endpoints directly

### If Database Connection Fails:
1. Check DATABASE_URL format
2. Verify PostgreSQL service is active
3. Check database logs in Railway
4. Ensure proper variable referencing

## 📝 Post-Deployment

### Optional Configurations:
- [ ] Set up custom domain
- [ ] Configure environment-specific settings
- [ ] Set up monitoring and alerts
- [ ] Configure automatic deployments
- [ ] Set up database backups

### Documentation:
- [ ] Update README with new deployment URLs
- [ ] Document environment variables
- [ ] Share access with team members

## 🆘 Getting Help

If you encounter issues:
1. Check Railway documentation: https://docs.railway.app
2. Review service logs in Railway dashboard
3. Join Railway Discord: https://discord.gg/railway
4. Check GitHub issues for common problems

## 📊 Expected Results

After successful deployment:
- **Backend URL**: `https://backend-production-xxxx.up.railway.app`
- **Frontend URL**: `https://frontend-production-xxxx.up.railway.app`  
- **Database**: Accessible via Railway dashboard
- **Data**: Initial roadmap data loaded automatically

## 💡 Tips for Success

1. **Deploy in Order**: Database → Backend → Frontend
2. **Check Logs**: Always check deployment logs for errors
3. **Environment Variables**: Use Railway's variable referencing for security
4. **Testing**: Test each service individually before integration
5. **Monitoring**: Set up alerts for service health

---

**Note**: Replace `[your-backend-url]` and `[frontend-url]` with actual URLs from Railway dashboard.
