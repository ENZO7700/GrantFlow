# GrantFlow Web (Next.js 15 PWA)

Dashboard podľa Blueprint §4 + napojenie na DNSH API (`grantflow-ai`).

## Spustenie

```powershell
# terminál 1 — AI API
cd ..\grantflow-ai
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8001

# terminál 2 — PWA
cd ..\web-app
copy .env.example .env.local
npm run dev
```

Otvor http://localhost:3000

## Env

| Premenná | Default |
|----------|---------|
| `NEXT_PUBLIC_API_URL` | `http://127.0.0.1:8001` |

## CTA

- **Spustiť DNSH Audit** → `POST /v1/dnsh/audit`
- **Pokračovať v písaní s AI** → placeholder (Agent 3)
- **Export ITMS2021+** → placeholder (US 6.2)

## Smoke

```powershell
npm run build
node scripts/smoke.mjs
```
