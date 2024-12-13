"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [analysis, setAnalysis] = useState("");
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login"); // Redirect if not logged in
    }

    // Fetch analysis data (mocked here for simplicity)
    setAnalysis("Here is your business analysis report!");
  }, [router]);

  const handleDownload = () => {
    const blob = new Blob([analysis], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "business_analysis.txt";
    link.click();
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <header className="bg-emerald-400 p-4 text-lime-50 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <button
          onClick={() => {
            localStorage.removeItem("token"); // Logout
            router.push("/login");
          }}
          className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800"
        >
          Logout
        </button>
      </header>

      <main className="mt-6">
        <h2 className="text-xl font-bold mb-4">Your Business Analysis</h2>
        <p className="bg-white p-4 rounded shadow">{analysis}</p>
        <button
          onClick={handleDownload}
          className="mt-4 bg-emerald-400 text-white px-4 py-2 rounded hover:bg-emerald-500"
        >
          Download Analysis
        </button>
      </main>
    </div>
  );
}
