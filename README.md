# GrantFlow (workspace)

Lokálny vývojový workspace pre GrantFlow.sk (Blueprint v2).

| Priečinok | Popis |
|-----------|--------|
| `grantflow-ai/` | FastAPI + LangGraph DNSH Auditor |
| `web-app/` | Next.js 15 dashboard PWA |
| `web/` | Zdrojové PWA ikony / static |
| `scripts/` | Pomocné skripty |
| `GrantFlow-SK-Blueprint-v2.*` | Blueprint exporty |

## Rýchly štart

```powershell
# Jedným príkazom (2 okná: API + PWA)
.\scripts\dev.ps1
```

Alebo manuálne:

```powershell
# terminál 1 — API
cd grantflow-ai
.\.venv\Scripts\activate
uvicorn app.main:app --reload --port 8001

# terminál 2 — UI
cd web-app
npm run dev
```

| Služba | URL |
|--------|-----|
| PWA | http://localhost:3000 |
| API OpenAPI | http://localhost:8001/docs |

## Prvé nastavenie (ak chýba)

```powershell
# AI
cd grantflow-ai
py -3.12 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
Copy-Item .env.example .env

# Web
cd ..\web-app
Copy-Item .env.example .env.local
npm install
```

## Overenie

```powershell
cd grantflow-ai; .\.venv\Scripts\pytest.exe -q
cd ..\web-app; npm run smoke
```
