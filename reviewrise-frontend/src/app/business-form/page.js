"use client";

import { useState } from "react";

export default function BusinessFormPage() {
  const [businessName, setBusinessName] = useState("");
  const [businessAddress, setBusinessAddress] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/business-info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ businessName, businessAddress }),
      });

      if (!response.ok) {
        throw new Error("Failed to submit business information");
      }

      alert("Business information submitted successfully!");
    } catch (error) {
      console.error(error);
      alert(error.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-6 rounded shadow-md w-full max-w-md"
      >
        <h2 className="text-2xl font-bold mb-4">Business Information</h2>

        <label className="block mb-2">Business Name</label>
        <input
          type="text"
          value={businessName}
          onChange={(e) => setBusinessName(e.target.value)}
          className="w-full p-2 border rounded mb-4"
          placeholder="Enter business name"
          required
        />

        <label className="block mb-2">Business Address</label>
        <input
          type="text"
          value={businessAddress}
          onChange={(e) => setBusinessAddress(e.target.value)}
          className="w-full p-2 border rounded mb-4"
          placeholder="Enter business address"
          required
        />

        <button className="px-4 py-2 bg-emerald-400 text-white rounded hover:bg-emerald-500">
          Submit
        </button>
      </form>
    </div>
  );
}
