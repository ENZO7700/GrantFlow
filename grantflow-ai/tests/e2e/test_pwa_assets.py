"""E2E checks for PWA assets (manifest + icons)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytestmark = pytest.mark.e2e

# Prefer Desktop package copy; fallback to Documents
CANDIDATES = [
    Path(r"C:\Users\42195\Desktop\TOP-PWA-H4CK3D-2026\projekt dotacione slovakia\web\public"),
    Path(r"C:\Users\42195\Documents\GrantFlow\web\public"),
]


@pytest.fixture(scope="module")
def public_dir() -> Path:
    for p in CANDIDATES:
        if p.exists() and (p / "manifest.webmanifest").exists():
            return p
    pytest.skip("web/public nenájdený")


REQUIRED_FILES = [
    "favicon.ico",
    "manifest.webmanifest",
    "index.html",
    "icons/favicon-16x16.png",
    "icons/favicon-32x32.png",
    "icons/apple-touch-icon.png",
    "icons/icon-192x192.png",
    "icons/icon-512x512.png",
    "icons/icon-512x512-maskable.png",
]


def test_all_pwa_files_exist(public_dir: Path) -> None:
    missing = [rel for rel in REQUIRED_FILES if not (public_dir / rel).exists()]
    assert not missing, f"Chýbajú súbory: {missing}"


def test_icons_not_empty(public_dir: Path) -> None:
    for rel in REQUIRED_FILES:
        if not rel.endswith((".png", ".ico")):
            continue
        size = (public_dir / rel).stat().st_size
        assert size > 100, f"{rel} je príliš malý ({size} B)"


def test_manifest_grantflow_schema(public_dir: Path) -> None:
    data = json.loads((public_dir / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert data["name"].startswith("GrantFlow")
    assert data["short_name"] == "GrantFlow"
    assert data["display"] == "standalone"
    assert data["theme_color"].upper() == "#0F172A"
    assert data["background_color"].upper() == "#0F172A"
    assert data["lang"] == "sk-SK"

    icons = data["icons"]
    sizes = {i["sizes"] for i in icons}
    assert "192x192" in sizes
    assert "512x512" in sizes
    purposes = {i.get("purpose") for i in icons}
    assert "any" in purposes
    assert "maskable" in purposes

    for icon in icons:
        src = icon["src"].lstrip("/")
        assert (public_dir / src).exists(), f"Manifest odkazuje na chýbajúci {src}"


def test_index_html_links_manifest(public_dir: Path) -> None:
    html = (public_dir / "index.html").read_text(encoding="utf-8")
    assert 'rel="manifest"' in html
    assert "manifest.webmanifest" in html
    assert "theme-color" in html
    assert "#0F172A" in html or "#0f172a" in html
