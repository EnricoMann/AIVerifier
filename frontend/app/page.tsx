"use client";

import { useState } from "react";
import ResultCard from "../components/ResultCard";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;

      const verifyRes = await fetch(`${apiUrl}/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (!verifyRes.ok) throw new Error(await verifyRes.text());
      const verifyData = await verifyRes.json();

      const analyzeRes = await fetch(`${apiUrl}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          claim: verifyData.claim,
          sources: verifyData.sources,
        }),
      });

      if (!analyzeRes.ok) throw new Error(await analyzeRes.text());
      const analyzeData = await analyzeRes.json();
      setResult(analyzeData);
    } catch (err: any) {
      console.error("❌ ERROR:", err);
      setError(err.message || "Unexpected error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center w-full">
      {/* Hero Section */}
      <section className="mt-10 sm:mt-16 text-center px-6">
        <h1 className="text-3xl sm:text-5xl font-extrabold text-gray-900 mb-2 tracking-tight">
          Analyze any claim with <span className="text-blue-600">AI</span>
        </h1>
        <p className="text-gray-600 max-w-2xl mx-auto text-base sm:text-lg">
          Powered by AI and trusted fact-checking sources.
        </p>
      </section>

      {/* Input Card */}
      <section className="w-full max-w-2xl mt-10 px-6">
        <div className="bg-white border border-gray-200 shadow-sm hover:shadow-md transition-shadow rounded-xl p-6">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">
            Paste a statement or headline:
          </h2>
          <textarea
            className="w-full border border-gray-300 p-3 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800"
            placeholder='Ex: "NASA confirms new life on Mars"'
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
          />

          <button
            onClick={handleVerify}
            disabled={loading}
            className={`mt-4 w-full p-3 rounded-lg font-semibold text-white transition-all duration-200 shadow-sm ${
              loading
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 active:scale-[0.98]"
            }`}
          >
            {loading ? (
              <span className="flex justify-center items-center gap-2">
                <svg
                  className="animate-spin h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  ></path>
                </svg>
                Verifying...
              </span>
            ) : (
              "Verify Claim"
            )}
          </button>
        </div>
      </section>

      {/* Status / Error */}
      <section className="mt-6 w-full max-w-2xl px-6 text-center">
        {error && (
          <div className="text-red-600 font-medium bg-red-50 border border-red-200 rounded-lg p-3 shadow-sm">
            ⚠️ {error}
          </div>
        )}

        {loading && !error && (
          <div className="text-gray-500 italic mt-4 animate-pulse">
            Checking trusted databases and analyzing results...
          </div>
        )}
      </section>

      {/* Results */}
      <section className="mt-10 w-full px-6 flex justify-center">
        {!loading && result && (
          <div className="animate-fadeIn">
            <ResultCard result={result} />
          </div>
        )}
      </section>
    </main>
  );
}