"use client";

import { useEffect, useState } from "react";

type HistoryItem = {
  id: number;
  claim: string;
  publisher: string;
  title: string;
  url: string;
  rating: string;
  summary: string;
  created_at: number;
};

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/history`);
      const data = await res.json();
      setItems(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const remove = async (id: number) => {
    if (!confirm("Delete this item?")) return;
    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/history/${id}`, { method: "DELETE" });
    setItems((prev) => prev.filter((i) => i.id !== id));
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <main className="min-h-screen bg-gray-50 p-6 flex justify-center">
      <div className="w-full max-w-3xl">
        <h1 className="text-2xl font-semibold mb-4">🕓 My History</h1>

        {loading && <p className="text-gray-500">Loading...</p>}

        {!loading && items.length === 0 && (
          <p className="text-gray-500">No saved items yet.</p>
        )}

        <div className="space-y-3">
          {items.map((i) => (
            <div key={i.id} className="bg-white border border-gray-200 rounded-lg p-4 shadow-sm">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-sm text-gray-500">
                    <span className="font-medium">Claim:</span> {i.claim}
                  </p>
                  <p className="font-semibold text-gray-900">{i.title}</p>
                  <p className="text-sm text-gray-700">{i.publisher} • {i.rating}</p>
                  {i.summary && (
                    <p className="text-sm text-gray-800 mt-2">{i.summary}</p>
                  )}
                  <a
                    href={i.url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-sm text-blue-600 hover:underline mt-2 inline-block"
                  >
                    View Source
                  </a>
                </div>
                <button
                  onClick={() => remove(i.id)}
                  className="text-xs text-red-600 border border-red-300 rounded px-2 py-1 hover:bg-red-50"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
