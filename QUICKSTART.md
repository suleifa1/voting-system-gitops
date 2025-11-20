# Quick Start Guide

## 🏗️ Project Structure

```
voting-system-gitops/
├── .github/workflows/          # CI/CD pipelines
│   ├── backend-build.yml      # Backend image build & push
│   └── frontend-build.yml     # Frontend image build & push
├── src/
│   ├── backend/
│   │   ├── Dockerfile         # Production (multi-stage, optimized)
│   │   └── Dockerfile.dev     # Development (hot reload)
│   └── frontend/
│       ├── Dockerfile         # Production (Next.js standalone)
│       └── Dockerfile.dev     # Development (dev server)
├── docker-compose.yml         # Development setup (with build context)
├── docker-compose.prod.yml    # Production setup (using GHCR images)
├── .env.example              # Environment variables template
└── GHCR_SETUP.md             # Detailed GHCR documentation
```

## 🚀 Quick Commands

### Development (Local)

```bash
# Start all services with hot reload
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Features:**
- ✅ Hot reload enabled
- ✅ Source code mounted as volumes
- ✅ Fast iteration

### Production (Using GHCR Images)

```bash
# Setup environment variables
cp .env.example .env
# Edit .env with your values

# Pull and run pre-built images
docker-compose -f docker-compose.prod.yml up

# Run in background
docker-compose -f docker-compose.prod.yml up -d

# Stop
docker-compose -f docker-compose.prod.yml down
```

**Features:**
- ✅ Production-ready images
- ✅ Multi-stage optimized builds
- ✅ Security hardened (non-root users)
- ✅ Health checks included

## 📦 Available Images

After pushing to GitHub `main` branch or creating a release:

- `ghcr.io/suleifa1/backend:latest` - Backend (FastAPI + Uvicorn)
- `ghcr.io/suleifa1/frontend:latest` - Frontend (Next.js standalone)

## 🔄 Workflow

### 1. Development Phase
```bash
# Make changes to code
vim src/backend/main.py

# Test locally
docker-compose up

# Commit and push
git add .
git commit -m "Add new feature"
git push origin feature-branch
```

### 2. Deploy to Dev/Staging
```bash
# Merge to main
git checkout main
git merge feature-branch
git push origin main

# GitHub Actions automatically builds and pushes images
# Wait for CI/CD to complete (~5-10 minutes)

# Pull latest images on your server
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### 3. Production Release
```bash
# Create release tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Or use GitHub UI: Releases → Create new release

# GitHub Actions builds versioned images
# Update production to use specific version:
# Edit docker-compose.prod.yml:
#   image: ghcr.io/suleifa1/backend:v1.0.0
```

## 🔍 Useful Commands

```bash
# Check running containers
docker ps

# View container logs
docker logs -f <container_id>

# Execute commands inside container
docker exec -it <container_id> /bin/sh

# Check image sizes
docker images | grep suleifa1

# Pull specific version
docker pull ghcr.io/suleifa1/backend:v1.0.0

# Clean up old images
docker image prune -a
```

## 🧪 Testing Images Locally

Before deploying to production, test pre-built images locally:

```bash
# Pull latest images
docker pull ghcr.io/suleifa1/backend:latest
docker pull ghcr.io/suleifa1/frontend:latest

# Run with production compose
docker-compose -f docker-compose.prod.yml up

# Test functionality
curl http://localhost:8000/docs  # Backend API docs
curl http://localhost:3000        # Frontend
```

## 📋 Next Steps

1. ✅ **Push to GitHub** - Images will be built automatically
2. ✅ **Check Actions tab** - Verify build success
3. ✅ **Test locally** - Use `docker-compose.prod.yml`
4. 🔜 **Setup Kubernetes** - Ready for k8s/ArgoCD deployment
5. 🔜 **Configure ArgoCD** - GitOps continuous deployment

## 📚 Documentation

- **Detailed GHCR Setup**: See [GHCR_SETUP.md](./GHCR_SETUP.md)
- **Backend API Docs**: http://localhost:8000/docs (when running)
- **CockroachDB Admin**: http://localhost:8080 (when running)

## 🆘 Troubleshooting

**Images not building?**
- Check GitHub Actions logs in the Actions tab
- Ensure workflow permissions are set correctly

**Can't pull images?**
- Make packages public in GitHub settings
- Or login: `echo $GITHUB_TOKEN | docker login ghcr.io -u suleifa1 --password-stdin`

**Backend health check failing?**
- Ensure `/health` endpoint exists in FastAPI app
- Or remove healthcheck from docker-compose temporarily

**Frontend build failing?**
- Check if `npm run build` works locally
- Ensure `output: 'standalone'` is in next.config.js
