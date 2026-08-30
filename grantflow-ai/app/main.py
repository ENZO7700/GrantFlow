"""GrantFlow AI — FastAPI entrypoint (DNSH Auditor skeleton)."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes_dnsh import router as dnsh_router
from app.config import settings

app = FastAPI(
    title="GrantFlow AI Orchestrator",
    description="RAG sub-agents skeleton — Agent 2 DNSH Auditor (§3.5 Blueprint v2)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dnsh_router, prefix="/v1/dnsh", tags=["DNSH"])

# PWA / favicon assets (Documents or Desktop package)
_WEB_PUBLIC_CANDIDATES = [
    Path(__file__).resolve().parents[2] / "web" / "public",
    Path(r"C:\Users\42195\Desktop\TOP-PWA-H4CK3D-2026\projekt dotacione slovakia\web\public"),
]
_WEB_PUBLIC = next((p for p in _WEB_PUBLIC_CANDIDATES if p.is_dir()), None)
if _WEB_PUBLIC is not None:
    _icons = _WEB_PUBLIC / "icons"
    if _icons.is_dir():
        app.mount("/icons", StaticFiles(directory=str(_icons)), name="icons")
    _FAVICON = _WEB_PUBLIC / "favicon.ico"
else:
    _FAVICON = None


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    if _FAVICON is not None and _FAVICON.exists():
        return FileResponse(str(_FAVICON), media_type="image/x-icon")
    return RedirectResponse(url="/docs")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "grantflow-ai", "mode": settings.llm_mode}
