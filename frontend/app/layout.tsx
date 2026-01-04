import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="corporate">
      <body
        className={`${inter.className} bg-zinc-50 text-zinc-900 antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
