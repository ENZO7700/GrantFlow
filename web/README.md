# GrantFlow — PWA ikony a Web App Manifest

Assety z `favicon_io` + GrantFlow branding podľa Blueprint §4.1.

## Súbory

```text
web/public/
  favicon.ico
  manifest.webmanifest
  index.html                 # lokálny náhľad
  icons/
    favicon-16x16.png
    favicon-32x32.png
    apple-touch-icon.png     # 180×180
    icon-192x192.png         # PWA any
    icon-512x512.png         # PWA any
    icon-512x512-maskable.png
    ATTRIBUTION.txt          # Twemoji CC-BY 4.0
web/manifest.ts.example      # pre Next.js App Router
```

## Theme

| Token | Hodnota |
|-------|---------|
| `theme_color` | `#0F172A` |
| `background_color` | `#0F172A` |
| Accent (UI) | `#2563EB` |
| `display` | `standalone` |
| `short_name` | `GrantFlow` |

## Next.js 15 — napojenie

1. Skopíruj obsah `public/` do koreňa Next app (`apps/web/public` alebo `web/public`).
2. Buď:
   - nechaj `public/manifest.webmanifest` a v `app/layout.tsx` pridaj:

```tsx
export const metadata = {
  applicationName: "GrantFlow",
  themeColor: "#0F172A",
  appleWebApp: {
    capable: true,
    title: "GrantFlow",
    statusBarStyle: "black-translucent",
  },
  icons: {
    icon: [
      { url: "/favicon.ico" },
      { url: "/icons/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/icons/icon-192x192.png", sizes: "192x192", type: "image/png" },
    ],
    apple: [{ url: "/icons/apple-touch-icon.png" }],
  },
  manifest: "/manifest.webmanifest",
};
```

   - alebo premenuj `manifest.ts.example` → `app/manifest.ts`.

3. Over Lighthouse PWA: ikony 192/512 + maskable, HTTPS, manifest.

## Lokálny náhľad

```powershell
cd web\public
npx --yes serve -p 5173
```

Otvor http://127.0.0.1:5173/

## Attribution

Ikonografika vychádza z Twemoji (CC-BY 4.0) — pozri `icons/ATTRIBUTION.txt`.
