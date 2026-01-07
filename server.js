import express from "express";
import fetch from "node-fetch";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

app.post("/chat", async (req, res) => {
  const { message } = req.body;

  if (!message) return res.status(400).json({ error: "Message vide" });

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini", // Modèle optimisé 2026
        messages: [
          { role: "system", content: "Tu es Marie, une professeure de français chaleureuse, claire et pédagogique pour des hispanophones." },
          { role: "user", content: message }
        ],
        max_tokens: 500
      })
    });

    const data = await response.json();
    
    if (data.error) throw new Error(data.error.message);

    const reply = data.choices[0].message.content;
    res.json({ reply });
  } catch (err) {
    console.error("Erreur API:", err.message);
    res.status(500).json({ error: "L'IA n'est pas disponible pour le moment." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Serveur prêt sur le port ${PORT}`));