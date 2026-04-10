import type { Metadata } from "next";
import { IBM_Plex_Sans, Source_Serif_4 } from "next/font/google";
import "./globals.css";

const uiSans = IBM_Plex_Sans({
  variable: "--font-ui-sans",
  subsets: ["latin"],
  weight: ["400", "500", "600"],
});

const articleSerif = Source_Serif_4({
  variable: "--font-article-serif",
  subsets: ["latin"],
  weight: ["400", "600", "700"],
});

export const metadata: Metadata = {
  title: {
    default: "LLM Knowledge Wiki",
    template: "%s | LLM Knowledge Wiki",
  },
  description:
    "A local-first markdown wiki rendered from the same files used by Obsidian, Codex, and Claude Code.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${uiSans.variable} ${articleSerif.variable}`}>
      <body>{children}</body>
    </html>
  );
}
