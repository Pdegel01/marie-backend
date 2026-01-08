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
  // On récupère le message actuel ET l'historique envoyé par le client
  const { message, history } = req.body;

  if (!message) return res.status(400).json({ error: "Message vide" });

  try {
    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          { 
            role: "system", 
            content: `Eres neoMarie, una profesora de francés experta para hispanohablantes. 
            Tu estilo es directo, amable y muy conciso.
            REGLAS ESTRICTAS:
            1. Tus respuestas NO deben superar las 2 o 3 frases.
            2. Ve directamente al grano, sin introducciones largas.
            3. Explica brevemente en español y da el ejemplo en francés.
            4. Si el usuario te habla en español, respóndele brevemente para guiarlo al francés.` 
          },
          // On injecte l'historique (tableau d'objets {role, content})
          ...(history || []), 
          // On ajoute le dernier message de l'utilisateur
          { role: "user", content: message }
        ],
        max_tokens: 150, 
        temperature: 0.7
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