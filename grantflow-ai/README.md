# GrantFlow AI Orchestrator — skeleton

FastAPI + LangGraph **Agent 2: DNSH Auditor** podľa Blueprint v2 (§3.2 / §3.5).

## Štruktúra

```
app/
  main.py                 # FastAPI
  config.py
  api/routes_dnsh.py      # POST /v1/dnsh/audit
  agents/
    dnsh_graph.py         # LangGraph: classify → evaluate → ground → aggregate → persist
    risk_classifier.py    # deterministické signály
    grounding.py          # grounding gate (§3.3)
  models/schemas.py       # DnshFinding / DnshAssessment
  services/
    retrieve_stub.py      # stub KB (neskôr pgvector)
    persist_stub.py       # jsonl store (neskôr Postgres)
```

## Spustenie

```bash
cd grantflow-ai
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

OpenAPI: http://localhost:8001/docs

### Príklad requestu

```bash
curl -X POST http://localhost:8001/v1/dnsh/audit ^
  -H "Content-Type: application/json" ^
  -d "{\"project_title\":\"FOVE hala\",\"project_brief\":\"Inštalácia fotovoltiky 100 kWp a batérií na streche výrobnej haly v BB.\",\"investment_types\":[\"fove\",\"battery\"]}"
```

## Testy

```bash
pytest -q
```

## Ďalšie kroky

1. Napojiť `retrieve_stub` na PostgreSQL + pgvector hybrid search.
2. Nahradiť `_decide_status` LLM structured output (Claude / GPT) pri zachovaní grounding gate.
3. Persist do tabuliek `dnsh_assessments` / `dnsh_findings`.
4. Pridať Agent 3 (Proposal Drafter) ako ďalší LangGraph subgraph.
