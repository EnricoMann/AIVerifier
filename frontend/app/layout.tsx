import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Verifier",
  description: "Check statements with AI and multiple fact-check APIs",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gradient-to-br from-gray-50 to-gray-100 text-gray-900 min-h-screen flex flex-col">
        {/* Navbar */}
        <header className="w-full bg-white shadow-sm fixed top-0 left-0 z-50">
          <nav className="max-w-5xl mx-auto px-6 py-3 flex justify-between items-center">
            <h1 className="text-lg font-semibold text-gray-800 tracking-tight">
              AI<span className="text-blue-600">Verifier</span>
            </h1>
            <div className="flex gap-4">
              <a
                href="/"
                className="text-sm text-gray-700 hover:text-blue-600 transition-colors"
              >
                Verify
              </a>
              <a
                href="/history"
                className="text-sm text-gray-700 hover:text-blue-600 transition-colors"
              >
                History
              </a>
            </div>
          </nav>
        </header>

        {/* Main Content */}
        <main className="flex-1 pt-20 pb-10 flex flex-col items-center">
          {children}
        </main>

        {/* Footer */}
        <footer className="text-center text-xs text-gray-500 py-4 border-t bg-white/70 backdrop-blur-sm">
          Built by{" "}
          <a
            href="https://github.com/EnricoMann"
            target="_blank"
            rel="noreferrer"
            className="font-medium text-blue-600 hover:text-blue-700 transition-colors"
          >
            Enrico Mann
          </a>
        </footer>
      </body>
    </html>
  );
}