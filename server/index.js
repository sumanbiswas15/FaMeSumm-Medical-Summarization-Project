const mongoose = require("mongoose");
const express = require("express");
const cors = require("cors");
const axios = require("axios");
require("dotenv").config();

const app = express(); // Initialize Express
app.use(express.json()); // Middleware to parse JSON requests
app.use(cors()); // Enable CORS

mongoose.connect("mongodb://127.0.0.1:27017/medical_summaries", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("✅ MongoDB Connected"))
  .catch(err => console.error("❌ MongoDB Connection Error:", err));

// Create a schema & model
const SummarySchema = new mongoose.Schema({
  text: String,
  summary: String,
  createdAt: { type: Date, default: Date.now }
});
const Summary = mongoose.model("Summary", SummarySchema);

// Route to fetch all summaries from MongoDB
app.get("/api/summaries", async (req, res) => {
  try {
    const allSummaries = await Summary.find().sort({ createdAt: -1 });
    res.json(allSummaries);
  } catch (error) {
    console.error("Error fetching summaries:", error);
    res.status(500).json({ error: "Failed to fetch summaries" });
  }
});

app.post("/api/summarize", async (req, res) => {
  try {
      const { text } = req.body;

      // Call FaMeSumm API (Ensure it's running)
      const response = await axios.post("http://127.0.0.1:8000/summarize", { text });

      // Check if response contains 'summary'
      if (!response.data || !response.data.summary) {
          throw new Error("Invalid response from FaMeSumm");
      }

      const summary = response.data.summary;

      // Save to MongoDB
      const newSummary = new Summary({ text, summary });
      await newSummary.save();

      res.json({ summary });
  } catch (error) {
      console.error("❌ Error generating summary:", error.message);
      res.status(500).json({ error: "Failed to generate summary" });
  }
});



// Start the server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`));
