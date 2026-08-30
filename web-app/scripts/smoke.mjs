/**
 * Smoke checks for GrantFlow web-app (no browser required).
 * Run after `npm run build` or with public/ present.
 */
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const required = [
  "public/favicon.ico",
  "public/manifest.webmanifest",
  "public/icons/icon-192x192.png",
  "public/icons/icon-512x512.png",
  "public/icons/icon-512x512-maskable.png",
  "public/icons/apple-touch-icon.png",
  "src/app/page.tsx",
  "src/lib/api.ts",
];

let failed = 0;
for (const rel of required) {
  const p = join(root, rel);
  if (!existsSync(p)) {
    console.error("MISSING", rel);
    failed += 1;
  } else {
    console.log("OK", rel);
  }
}

const manifest = JSON.parse(
  readFileSync(join(root, "public/manifest.webmanifest"), "utf8"),
);
if (manifest.short_name !== "GrantFlow") {
  console.error("FAIL manifest.short_name");
  failed += 1;
} else {
  console.log("OK manifest.short_name");
}

const api = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001";
try {
  const res = await fetch(`${api}/health`);
  const body = await res.json();
  if (res.ok && body.status === "ok") {
    console.log("OK API health", api);
  } else {
    console.warn("WARN API health not ok (start uvicorn for full stack)", res.status);
  }
} catch {
  console.warn("WARN API unreachable (optional for static smoke)", api);
}

if (failed > 0) {
  console.error(`Smoke failed: ${failed} issue(s)`);
  process.exit(1);
}
console.log("Smoke passed");
