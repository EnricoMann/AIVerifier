"use client";

import { useState } from "react";

type SummaryItem = {
  publisher: string;
  title: string;
  url: string;
  rating: string;
  summary?: string;
};

export default function ResultCard({
  result,
}: {
  result: { claim: string; summaries: SummaryItem[] };
}) {
  const [open, setOpen] = useState<Record<number, boolean>>({});
  const [saving, setSaving] = useState<Record<number, boolean>>({});
  const [saved, setSaved] = useState<Record<number, boolean>>({});

  const toggle = (idx: number) =>
    setOpen((prev) => ({ ...prev, [idx]: !prev[idx] }));

  const saveItem = async (idx: number, item: SummaryItem) => {
    if (saved[idx]) return;
    try {
      setSaving((s) => ({ ...s, [idx]: true }));
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/history`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          claim: result.claim,
          publisher: item.publisher,
          title: item.title,
          url: item.url,
          rating: item.rating,
          summary: item.summary || "",
        }),
      });
      if (!res.ok) throw new Error(await res.text());
      setSaved((s) => ({ ...s, [idx]: true }));
    } catch (e) {
      console.error("Failed to save:", e);
      alert("Failed to save to history.");
    } finally {
      setSaving((s) => ({ ...s, [idx]: false }));
    }
  };

  if (!result?.summaries?.length) return null;

  return (
    <div className="w-full max-w-3xl space-y-6 animate-fadeIn">
      <h2 className="text-xl font-semibold text-gray-800 mb-2">
        Results for:{" "}
        <span className="text-blue-600 font-bold">{result.claim}</span>
      </h2>

      {result.summaries.map((item, idx) => (
        <div
          key={`${item.url}-${idx}`}
          className="bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200 p-5"
        >
          {/* Info */}
          <div className="flex items-start justify-between flex-wrap gap-4">
            <div className="flex-1 min-w-[220px]">
              <p className="font-semibold text-gray-900">{item.publisher}</p>
              <p className="text-sm text-gray-800 leading-snug mt-0.5">
                {item.title}
              </p>
              <p className="text-xs text-gray-500 mt-1">
                <span className="italic">Rating:</span>{" "}
                <span className="font-medium">{item.rating}</span>
              </p>
            </div>

            {/* Buttons */}
            <div className="flex flex-col sm:flex-row sm:items-center gap-2 shrink-0 text-sm">
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className="px-3 py-1 border border-blue-200 text-blue-600 font-medium rounded-md hover:bg-blue-50 transition-colors"
              >
                View Source ↗
              </a>

              <button
                onClick={() => toggle(idx)}
                className="px-3 py-1 border border-gray-200 rounded-md text-gray-700 hover:text-blue-600 hover:border-blue-300 transition-colors"
              >
                {open[idx] ? "Hide AI Summary" : "Show AI Summary"}
              </button>

              <button
                disabled={saved[idx] || saving[idx]}
                onClick={() => saveItem(idx, item)}
                className={`px-3 py-1 rounded-md border text-xs font-medium transition-colors ${
                  saved[idx]
                    ? "text-green-700 border-green-300 bg-green-50 cursor-default"
                    : saving[idx]
                    ? "text-blue-600 border-blue-300 bg-blue-50 animate-pulse"
                    : "text-gray-700 border-gray-300 hover:bg-gray-50"
                }`}
              >
                {saved[idx]
                  ? "Saved ✓"
                  : saving[idx]
                  ? "Saving..."
                  : "Save to my history"}
              </button>
            </div>
          </div>

          {/* Summary */}
          {open[idx] && item.summary && (
            <div className="mt-4 p-3 rounded-lg bg-blue-50 text-gray-800 text-sm leading-relaxed border border-blue-100">
              {item.summary}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}