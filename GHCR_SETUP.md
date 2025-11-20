# GitHub Container Registry (GHCR) Setup Guide

This guide explains how to use the GitHub Actions CI/CD pipeline to build and push Docker images to GitHub Container Registry.

## 📦 Container Images

After pushing to `main` or creating a release, the following images will be available:

- **Backend**: `ghcr.io/suleifa1/backend`
- **Frontend**: `ghcr.io/suleifa1/frontend`

## 🏷️ Image Tagging Strategy

### Push to `main` branch:
- `ghcr.io/suleifa1/backend:latest`
- `ghcr.io/suleifa1/backend:sha-abc123` (commit SHA)

### Release (e.g., `v1.0.0`):
- `ghcr.io/suleifa1/backend:v1.0.0`
- `ghcr.io/suleifa1/backend:1.0`
- `ghcr.io/suleifa1/backend:1`
- `ghcr.io/suleifa1/backend:latest`

## 🚀 GitHub Actions Workflows

Two workflows are configured:

1. **`.github/workflows/backend-build.yml`** - Builds backend (FastAPI)
2. **`.github/workflows/frontend-build.yml`** - Builds frontend (Next.js)

### Triggers:
- **Push to `main`**: Builds and tags as `latest` + `sha-xxx`
- **Release published**: Builds and tags with semantic version

### Multi-platform Support:
- `linux/amd64` (x86_64 servers, Intel Macs)
- `linux/arm64` (ARM servers, Apple Silicon M1/M2/M3)

## 🔐 Setup Requirements

### 1. Enable GitHub Container Registry

GitHub Container Registry is enabled by default, but you need to ensure packages are accessible:

1. Go to your repository settings
2. Navigate to **Actions** → **General**
3. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

### 2. Make Images Public (Optional)

After the first build:

1. Go to https://github.com/users/suleifa1/packages
2. Find your package (backend/frontend)
3. Click **Package settings**
4. Scroll to **Danger Zone**
5. Click **Change visibility** → **Public**

This allows pulling images without authentication.

## 📝 How to Use

### Development (Local):

```bash
# Uses Dockerfile.dev with hot reload and volumes
docker-compose up --build
```

### Production (Pre-built images):

```bash
# Pull and run images from GHCR
docker-compose -f docker-compose.prod.yml up
```

### Specify Version:

Edit `docker-compose.prod.yml` to use a specific version:

```yaml
backend:
  image: ghcr.io/suleifa1/backend:v1.0.0  # Instead of :latest
```

## 🔄 Workflow Process

### For Development:
1. Make changes to code
2. Commit and push to feature branch
3. Create PR to `main`
4. Merge PR → triggers image build
5. Images tagged as `latest`

### For Production Release:
1. Ensure `main` is stable
2. Create a new release on GitHub:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. Or use GitHub UI: Releases → Create new release
4. GitHub Actions builds and pushes versioned images

## 🔍 Verifying Images

Check if images were pushed successfully:

```bash
# List all tags for backend
gh api /users/suleifa1/packages/container/backend/versions

# Pull specific image
docker pull ghcr.io/suleifa1/backend:latest

# Inspect image
docker inspect ghcr.io/suleifa1/backend:latest
```

## 🐳 Dockerfile Structure

### Production Dockerfiles:
- `src/backend/Dockerfile` - Multi-stage, optimized, runs uvicorn
- `src/frontend/Dockerfile` - Multi-stage, standalone Next.js build

### Development Dockerfiles:
- `src/backend/Dockerfile.dev` - Hot reload with volumes
- `src/frontend/Dockerfile.dev` - Next.js dev server

## 🎯 ArgoCD Integration (Future)

These images are ready for Kubernetes/ArgoCD deployment:

```yaml
# k8s/backend-deployment.yml
spec:
  containers:
  - name: backend
    image: ghcr.io/suleifa1/backend:v1.0.0  # Use specific version
    # Or for dev environment:
    # image: ghcr.io/suleifa1/backend:latest
```

## 🛠️ Troubleshooting

### Build failing?

Check GitHub Actions logs:
- Go to **Actions** tab in GitHub
- Click on failed workflow
- Check build logs

### Can't pull image?

```bash
# Login to GHCR (if image is private)
echo $GITHUB_TOKEN | docker login ghcr.io -u suleifa1 --password-stdin

# Pull image
docker pull ghcr.io/suleifa1/backend:latest
```

### Image not updating?

- Ensure workflow completed successfully
- Check if you're using `:latest` tag (may be cached)
- Use specific SHA tag: `ghcr.io/suleifa1/backend:sha-abc123`

## 📊 CI/CD Pipeline Features

✅ Multi-stage builds (smaller images)  
✅ Multi-platform (AMD64 + ARM64)  
✅ Layer caching (faster builds)  
✅ Semantic versioning  
✅ Security: non-root users  
✅ Health checks included  
✅ Auto-triggered on push/release  

## 🔗 Useful Links

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Your GHCR Packages](https://github.com/users/suleifa1/packages)
