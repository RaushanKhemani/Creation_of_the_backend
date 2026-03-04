$ErrorActionPreference = "Stop"

Write-Host "[1/6] Moving to project folder..."
Set-Location "C:\Users\ASUS\Desktop\ai-hub-backend"

Write-Host "[2/6] Running health check..."
python -c "from fastapi.testclient import TestClient; from app import app; c=TestClient(app); r=c.get('/api/v1/health'); print('health:', r.status_code, r.json()['success'])"

Write-Host "[3/6] Running readiness check..."
python -c "from fastapi.testclient import TestClient; from app import app; c=TestClient(app); r=c.get('/api/v1/health/ready'); print('ready:', r.status_code, r.json()['data']['status'])"

Write-Host "[4/6] Running auth check..."
python -c "import uuid; from fastapi.testclient import TestClient; from app import app; c=TestClient(app); e=f'smoke_{uuid.uuid4().hex[:8]}@example.com'; p='StrongPass123'; reg=c.post('/api/v1/auth/register', json={'email':e,'password':p,'full_name':'Smoke User'}); login=c.post('/api/v1/auth/login', json={'email':e,'password':p}); print('register:', reg.status_code, 'login:', login.status_code)"

Write-Host "[5/6] Running provider + key activation check..."
python -c "import uuid; from fastapi.testclient import TestClient; from app import app; c=TestClient(app); e=f'smoke_{uuid.uuid4().hex[:8]}@example.com'; p='StrongPass123'; c.post('/api/v1/auth/register', json={'email':e,'password':p,'full_name':'Smoke User'}); t=c.post('/api/v1/auth/login', json={'email':e,'password':p}).json()['data']['access_token']; h={'Authorization':f'Bearer {t}'}; k=c.post('/api/v1/integrations/api-key', json={'api_key':'sk-smoke-key-123456789'}, headers=h); pr=c.get('/api/v1/providers', headers=h); print('api_key:', k.status_code, 'providers:', pr.status_code)"

Write-Host "[6/6] Running chat check..."
python -c "import uuid; from fastapi.testclient import TestClient; from app import app; c=TestClient(app); e=f'smoke_{uuid.uuid4().hex[:8]}@example.com'; p='StrongPass123'; c.post('/api/v1/auth/register', json={'email':e,'password':p,'full_name':'Smoke User'}); t=c.post('/api/v1/auth/login', json={'email':e,'password':p}).json()['data']['access_token']; h={'Authorization':f'Bearer {t}'}; c.post('/api/v1/integrations/api-key', json={'api_key':'sk-smoke-key-123456789'}, headers=h); rr=c.post('/api/v1/chat/route', json={'prompt':'Smoke test prompt'}, headers=h); print('chat_route:', rr.status_code, 'has_data:', rr.json().get('success'))"

Write-Host "Smoke check completed."
