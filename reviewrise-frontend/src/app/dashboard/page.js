"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [url, setUrl] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const router = useRouter();

  // Check for token on page load
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      // Redirect to login if no token is found
      router.push("/login");
    }
  }, [router]);

  // Handle the website analysis request
  const handleAnalyze = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setAnalysis(null);

    try {
      const token = localStorage.getItem("token");
      if (!token) throw new Error("You are not logged in. Please log in first.");

      const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token, // Pass the token to the backend
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || "Analysis failed");
      }

      const data = await response.json();
      setAnalysis(data.analysis);
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-lime-50 p-6">
      {/* Header */}
      <header className="bg-emerald-400 p-4 text-lime-50 flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <button
          onClick={handleLogout}
          className="bg-emerald-900 text-lime-50 px-4 py-2 rounded-xl hover:bg-emerald-800"
        >
          Logout
        </button>
      </header>

      {/* Main Content */}
      <main className="text-emerald-900 mt-6">
        <form onSubmit={handleAnalyze} className="mb-4">
          <label className="block mb-2">Enter Your Website URL:</label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full p-2 border rounded mb-4"
            placeholder="https://yourwebsite.com"
            required
          />
          <button
            type="submit"
            className="px-4 py-2 bg-emerald-400 text-lime-50 rounded-lg hover:bg-emerald-500"
          >
            Analyze
          </button>
        </form>

        {/* Loading State */}
        {loading && <p className="mt-4 text-emerald-900">🤖 Analyzing your website...</p>}

        {/* Error Message */}
        {message && <p className="mt-4 text-red-500">{message}</p>}

        {/* Display Analysis Results */}
        {analysis && (
          <div className="mt-6 bg-emerald-200 p-4 text-black rounded-xl shadow-md">
            <h3 className="text-xl font-bold mb-2">Analysis Results</h3>
            <p>
              <strong>Title:</strong> {analysis.title}
            </p>
            <p>
              <strong>Total Word Count:</strong> {analysis.word_count}
            </p>
            <p>
              <strong>Website Preview:</strong> {analysis.text_preview}
            </p>

            <div className="mt-4">
              <h4 className="text-lg font-bold mb-2">Analysis Summary</h4>
              <p className="whitespace-pre-line">{analysis.ai_analysis}</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
