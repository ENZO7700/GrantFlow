import type { Metadata, Viewport } from "next";
import { Outfit, Sora } from "next/font/google";
import "./globals.css";

const outfit = Outfit({
  variable: "--font-outfit",
  subsets: ["latin", "latin-ext"],
});

const sora = Sora({
  variable: "--font-sora",
  subsets: ["latin", "latin-ext"],
  weight: ["500", "600", "700"],
});

export const metadata: Metadata = {
  title: {
    default: "GrantFlow Slovensko",
    template: "%s · GrantFlow",
  },
  description:
    "EU dotácie a granty pre slovenské MSP — match výziev, AI Copilot a DNSH audit.",
  applicationName: "GrantFlow",
  manifest: "/manifest.webmanifest",
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
      { url: "/icons/icon-512x512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: [{ url: "/icons/apple-touch-icon.png" }],
  },
};

export const viewport: Viewport = {
  themeColor: "#0F172A",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="sk">
      <body className={`${outfit.variable} ${sora.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
