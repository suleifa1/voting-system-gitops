# Kubernetes Deployment Guide

## 📋 Структура манифестов

```
k8s/
├── namespace.yml              # Namespace voting-system
├── configmap.yml              # ConfigMap с env переменными
├── secret.yml                 # Secret с SECRET_KEY
├── cockroachdb/
│   ├── statefulset.yml       # CockroachDB single-node
│   └── service.yml           # ClusterIP service (26257, 8080)
├── backend/
│   ├── deployment.yml        # Backend API (2 реплики)
│   └── service.yml           # ClusterIP service (8000)
└── frontend/
    ├── deployment.yml        # Frontend Next.js (2 реплики)
    └── service.yml           # LoadBalancer service (80 → 3000)
```

## 🚀 Деплой в Minikube

### 1. Убедитесь что Minikube запущен:

```bash
minikube status
kubectl get nodes
```

### 2. Примените манифесты в правильном порядке:

```bash
# Namespace
kubectl apply -f k8s/namespace.yml

# ConfigMap и Secret
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/secret.yml

# База данных (первая!)
kubectl apply -f k8s/cockroachdb/

# Backend
kubectl apply -f k8s/backend/

# Frontend
kubectl apply -f k8s/frontend/
```

### 3. Проверьте статус:

```bash
# Все ресурсы в namespace
kubectl get all -n voting-system

# Pod'ы
kubectl get pods -n voting-system

# Services
kubectl get svc -n voting-system

# StatefulSet
kubectl get statefulset -n voting-system
```

### 4. Дождитесь пока все Pod'ы будут Ready:

```bash
kubectl get pods -n voting-system -w
# Ctrl+C чтобы выйти
```

Должно быть:
- `cockroachdb-0` - Running (1/1)
- `backend-xxx-xxx` - Running (1/1) x2
- `frontend-xxx-xxx` - Running (1/1) x2

### 5. Получите внешний IP frontend:

```bash
# Для Minikube нужен tunnel:
minikube tunnel
# Держите открытым в отдельном терминале!

# Или используйте minikube service:
minikube service frontend -n voting-system
```

## 📊 Полезные команды

### Логи:

```bash
# Логи Backend
kubectl logs -f deployment/backend -n voting-system

# Логи Frontend
kubectl logs -f deployment/frontend -n voting-system

# Логи CockroachDB
kubectl logs -f cockroachdb-0 -n voting-system
```

### Подключение к контейнерам:

```bash
# Подключиться к Backend
kubectl exec -it deployment/backend -n voting-system -- /bin/bash

# Подключиться к CockroachDB
kubectl exec -it cockroachdb-0 -n voting-system -- /bin/bash

# SQL в CockroachDB
kubectl exec -it cockroachdb-0 -n voting-system -- \
  ./cockroach sql --insecure -e "SELECT * FROM users;"
```

### Масштабирование:

```bash
# Увеличить реплики backend
kubectl scale deployment/backend --replicas=3 -n voting-system

# Уменьшить реплики frontend
kubectl scale deployment/frontend --replicas=1 -n voting-system
```

### Обновление образов:

```bash
# После нового push в GHCR
kubectl rollout restart deployment/backend -n voting-system
kubectl rollout restart deployment/frontend -n voting-system

# Статус rolling update
kubectl rollout status deployment/backend -n voting-system
```

### Port Forward (для тестирования):

```bash
# Backend API
kubectl port-forward svc/backend 8000:8000 -n voting-system
# http://localhost:8000/docs

# CockroachDB Admin UI
kubectl port-forward svc/cockroachdb 8080:8080 -n voting-system
# http://localhost:8080
```

## 🛑 Удаление

```bash
# Удалить всё приложение
kubectl delete namespace voting-system

# Или по частям:
kubectl delete -f k8s/frontend/
kubectl delete -f k8s/backend/
kubectl delete -f k8s/cockroachdb/
kubectl delete -f k8s/configmap.yml
kubectl delete -f k8s/secret.yml
kubectl delete -f k8s/namespace.yml
```

## 🔧 Troubleshooting

### Pod не запускается:

```bash
# Описание Pod'а
kubectl describe pod <pod-name> -n voting-system

# События
kubectl get events -n voting-system --sort-by='.lastTimestamp'
```

### ImagePullBackOff:

```bash
# Проверить образы доступны
docker pull ghcr.io/suleifa1/backend:latest
docker pull ghcr.io/suleifa1/frontend:latest

# Или сделать образы публичными на GitHub
```

### CrashLoopBackOff Backend:

```bash
# Проверить логи
kubectl logs <backend-pod> -n voting-system

# Проверить что CockroachDB готов
kubectl get pods -n voting-system | grep cockroachdb

# Проверить env переменные
kubectl exec <backend-pod> -n voting-system -- env | grep DB_
```

## 📝 Важные заметки

1. **SECRET_KEY**: Замените в `k8s/secret.yml` на свой!
   ```bash
   python3 -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

2. **LoadBalancer в Minikube**: Требует `minikube tunnel` или используйте `minikube service`

3. **Образы**: Убедитесь что образы в GHCR публичные или настройте imagePullSecrets

4. **База данных**: PersistentVolume создаётся автоматически через StorageClass

5. **Миграции**: Нужно будет запустить Alembic миграции после старта БД
