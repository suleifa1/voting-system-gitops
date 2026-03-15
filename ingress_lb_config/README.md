# Ingress Load Balancer Configuration

This directory contains NGINX Ingress Controller configurations with dedicated IP addresses for each namespace (staging, prod) allocated by **MetalLB**.

## Structure

```
ingress_lb_config/
├── prod/          # NGINX Ingress Controller for production
│   ├── ingressclass-prod.yaml              # IngressClass "nginx-prod"
│   ├── ingress-nginx-prod-rbac.yaml        # RBAC permissions
│   ├── ingress-nginx-controller-prod-service.yaml  # LoadBalancer Service (MetalLB IP from prod-pool)
│   └── ingress-nginx-controller-prod-deployment.yaml  # NGINX controller
└── staging/       # NGINX Ingress Controller for staging
    ├── ingressclass-staging.yaml
    ├── ingress-nginx-staging-rbac.yaml
    ├── ingress-nginx-controller-staging-service.yaml  # LoadBalancer Service (MetalLB IP from staging-pool)
    └── ingress-nginx-controller-staging-deployment.yaml
```

## Purpose

Each namespace (staging, prod) has its **own NGINX Ingress Controller** with a **dedicated LoadBalancer Service**, providing:
- Different IP addresses for staging and prod (allocated by MetalLB)
- Independent load balancing
- Configuration isolation
- Environment-specific SSL certificates

## MetalLB Integration

LoadBalancer Services get external IPs from **MetalLB** pools:

```
┌─────────────────────────────────────────┐
│  LoadBalancer Services (staging/prod)   │
│   ingress-nginx-controller-{env}        │
└──────────────┬──────────────────────────┘
               │
        ┌──────▼─────┐
        │   MetalLB  │
        │  IP Pools: │
        ├────────────┤
        │ app-pool   │ → x.x.x.x
        └────────────┘
```


**Requirements:**
- MetalLB must be installed in cluster
- Address pools configured for staging and prod separetely or just defined like a range of IPs
- Network capable of routing allocated IPs

## Deployment

### For Staging:
```bash
kubectl apply -f ingress_lb_config/staging/ingressclass-staging.yaml
kubectl apply -f ingress_lb_config/staging/ingress-nginx-staging-rbac.yaml
kubectl apply -f ingress_lb_config/staging/ingress-nginx-controller-staging-deployment.yaml
kubectl apply -f ingress_lb_config/staging/ingress-nginx-controller-staging-service.yaml
```

### For Production:
```bash
kubectl apply -f ingress_lb_config/prod/ingressclass-prod.yaml
kubectl apply -f ingress_lb_config/prod/ingress-nginx-prod-rbac.yaml
kubectl apply -f ingress_lb_config/prod/ingress-nginx-controller-prod-deployment.yaml
kubectl apply -f ingress_lb_config/prod/ingress-nginx-controller-prod-service.yaml
```

## Getting IP Address (Assigned by MetalLB)

```bash
# Staging (IP from app-pool)
kubectl get svc -n ingress-nginx-staging ingress-nginx-controller-staging
# Example output: 10.0.100.50

# Production (IP from app-pool)
kubectl get svc -n ingress-nginx-prod ingress-nginx-controller-prod
# Example output: 10.0.200.50
```

## Specifying Fixed IP Address

To assign a **specific IP from MetalLB pool** to a LoadBalancer Service, use the `metallb.universe.tf/loadBalancerIPs` annotation:

### Example - Staging Service with Fixed IP:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ingress-nginx-controller-staging
  namespace: ingress-nginx-staging
  annotations:
    metallb.universe.tf/loadBalancerIPs: 10.0.100.50  # Define an IP from app-pool in MetalLB
spec:
  type: LoadBalancer
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/component: controller
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: 80
    - name: https
      port: 443
      protocol: TCP
      targetPort: 443
```

### Requirements:
- IP must be within the configured MetalLB pool range
- IP must not be already allocated to another service
- MetalLB will reject invalid IPs with an error

### Without Fixed IP (Auto-allocation):

If you don't specify the annotation, MetalLB will automatically assign the next available IP from the pool.



## Notes

These configurations:
- Are **NOT** included in the Helm chart (applied separately)
- **Must not be** applied before Helm deployment (they are not a dependency, just an optional solution for cross branch deployment in 1 cluster)
- Can be deployed in CI/CD pipeline pre-deployment stage
- Serve as reference/artifacts for infrastructure documentation
- **Require MetalLB** to be installed and configured with IP pools
