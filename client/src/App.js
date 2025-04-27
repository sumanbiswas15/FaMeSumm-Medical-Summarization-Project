import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSummarize = async () => {
    if (!text.trim()) {
      setError("⚠️ Please enter medical text to summarize.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/summarize", { text });
      console.log("🟢 API Response:", response.data);
      setResponseData(response.data);
    } catch (err) {
      console.error("❌ Error generating summary:", err);
      setError("⚠️ Failed to generate summary. Try again.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gray-100 p-8">
      <h1 className="text-4xl font-extrabold text-center text-blue-700 mb-6">
        Medical Text Summarization
      </h1>

      {error && <p className="text-red-500 text-center bg-red-100 p-2 rounded-md w-full">{error}</p>}

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="📝 Enter medical text here..."
        rows="10"
        className="w-full h-48 p-4 border border-gray-400 rounded-lg shadow-md focus:ring-2 focus:ring-blue-500 focus:outline-none resize-none"
      />
      <br></br>

      <button
        onClick={handleSummarize}
        className="mt-4 bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 
        text-white font-semibold py-3 px-8 rounded-lg shadow-lg transform transition-all hover:scale-105"
        disabled={loading}
      >
        {loading ? "⏳ Summarizing..." : "✨ Summarize"}
      </button>

      {loading && <p className="text-center text-blue-500 mt-3">Processing summary...</p>}

      {responseData && (
        <div className="mt-6 p-6 bg-white shadow-lg rounded-lg w-full border border-gray-200">
          <h2 className="text-2xl font-bold text-blue-600">📋 Extracted Summary:</h2>
          <p className="mt-2"><strong>👤 Patient Info:</strong> {responseData.Patient_Info || "Unknown"}</p>
          <p className="mt-2"><strong>🩺 Diagnosis:</strong> {responseData.Diagnosis?.join(", ") || "Not specified"}</p>
          <p className="mt-2"><strong>🔬 Procedure:</strong> {responseData.Procedure?.join(", ") || "Not specified"}</p>
          <p className="mt-2"><strong>💊 Medications:</strong> {responseData.Medications?.join(", ") || "Not specified"}</p>
          <p className="mt-2 text-gray-800"><strong>📝 Summary:</strong> {responseData.Summary || "No summary available"}</p>
        </div>
      )}
    </div>
  );
}

export default App;
