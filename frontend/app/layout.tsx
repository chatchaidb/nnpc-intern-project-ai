// Root layout — global styles and page chrome.
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NNPC AI Agents",
  description: "Internal chat UI for the NNPC / Chin Chun agent team",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
