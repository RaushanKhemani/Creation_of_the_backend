$ErrorActionPreference = "Stop"

Write-Host "[1/6] Moving to project folder..."
Set-Location "C:\Users\ASUS\Desktop\ai-hub-backend"

Write-Host "[2/6] Running in-process health check..."
python -c "from fastapi.testclient import TestClient; from app import app; c=TestClient(app); r=c.get('/api/v1/health'); print('health:', r.status_code, r.json().get('status'))"

Write-Host "[3/6] Running readiness check..."
python -c "from fastapi.testclient import TestClient; from app import app; c=TestClient(app); r=c.get('/api/v1/health/ready'); print('ready:', r.status_code, r.json().get('status'))"

Write-Host "[4/6] Running auth flow check..."
python -c "import uuid; from fastapi.testclient import TestClient; from app import app; c=TestClient(app); e=f'smoke_{uuid.uuid4().hex[:8]}@example.com'; p='StrongPass123'; reg=c.post('/api/v1/auth/register', json={'email':e,'password':p,'full_name':'Smoke User'}); login=c.post('/api/v1/auth/login', json={'email':e,'password':p}); print('register:', reg.status_code, 'login:', login.status_code)"

Write-Host "[5/6] Running protected providers check..."
python -c "import uuid; from fastapi.testclient import TestClient; from app import app; c=TestClient(app); e=f'smoke_{uuid.uuid4().hex[:8]}@example.com'; p='StrongPass123'; c.post('/api/v1/auth/register', json={'email':e,'password':p,'full_name':'Smoke User'}); t=c.post('/api/v1/auth/login', json={'email':e,'password':p}).json()['access_token']; r=c.get('/api/v1/providers', headers={'Authorization':f'Bearer {t}'}); print('providers:', r.status_code, 'count:', len(r.json()) if r.status_code==200 else 'n/a')"

Write-Host "[6/6] Running chat route check..."
python -c "import uuid; from fastapi.testclient import TestClient; from app import app; c=TestClient(app); e=f'smoke_{uuid.uuid4().hex[:8]}@example.com'; p='StrongPass123'; c.post('/api/v1/auth/register', json={'email':e,'password':p,'full_name':'Smoke User'}); t=c.post('/api/v1/auth/login', json={'email':e,'password':p}).json()['access_token']; h={'Authorization':f'Bearer {t}'}; rr=c.post('/api/v1/chat/route', json={'provider_key':'chatgpt','prompt':'Smoke test prompt'}, headers=h); ok='yes' if rr.status_code==200 else 'no'; print('chat_route:', rr.status_code, 'ok:', ok)"

Write-Host "Smoke check completed."
