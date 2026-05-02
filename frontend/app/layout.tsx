import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PropIntel AI Copilot",
  description: "Autonomous Lending Intelligence & Risk Simulation",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
