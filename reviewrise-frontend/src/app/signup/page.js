"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignupPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const router = useRouter();

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.message || "Signup failed");
      }

      setMessage("Signup successful! Redirecting...");
      setTimeout(() => {
        router.push("/login");
      }, 1000);
    } catch (err) {
      setMessage(err.message);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-lime-50">
      <form
        onSubmit={handleSignup}
        className="bg-emerald-400 p-10 rounded-3xl shadow-md w-full max-w-sm"
      >
        <h2 className="text-2xl font-bold mb-4 text-lime-50">Signup</h2>
        <label className="block mb-2 text-lime-50">Username</label>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 border rounded mb-4 bg-lime-50"
          placeholder="Enter username"
          required
        />
        <label className="block mb-2 text-lime-50">Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 border rounded mb-4 bg-lime-50"
          placeholder="Enter password"
          required
        />
        <button
          type="submit"
          className="bg-emerald-900 text-white px-4 py-2 rounded-xl hover:bg-emerald-300"
        >
          Signup
        </button>
        {message && (
          <p className="mt-4 text-sm text-lime-50 bg-emerald-900 p-2 rounded-lg">
            {message}
          </p>
        )}
      </form>
    </div>
  );
}
