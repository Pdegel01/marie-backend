import express from "express";
import fetch from "node-fetch";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY;

app.post("/chat", async (req, res) => {
  const { message, history } = req.body;

  if (!message) return res.status(400).json({ error: "Message vide" });

  // --- NOUVEAU : NETTOYAGE DE L'HISTORIQUE ---
  // On retire tous les messages qui n'ont pas de texte (content) pour éviter l'erreur "got null"
  const cleanHistory = (history || []).filter(msg => msg.content && msg.content.trim() !== "");

  try {
    // 1. APPEL À OPENAI POUR LE TEXTE
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
            content: `Eres neoMarie, una profesora de français experta...` // Ton prompt habituel
          },
          ...cleanHistory, // On utilise l'historique PROPRE ici
          { role: "user", content: message }
        ],
        max_tokens: 150, 
        temperature: 0.7
      })
    });
    const data = await response.json();
    if (data.error) throw new Error(data.error.message);

    const reply = data.choices[0].message.content;

    // --- 2. APPEL À ELEVENLABS POUR LA VOIX (Koraly) ---
    const voiceId = "rbFGGoDXFHtVghjHuS3E"; // <--- ID DE KORALY MIS À JOUR ICI
    const ttsResponse = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
      method: "POST",
      headers: {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: reply,
        model_id: "eleven_multilingual_v2", 
        voice_settings: {
          stability: 0.5,
          similarity_boost: 0.75
        }
      })
    });

    if (!ttsResponse.ok) {
        const errorDetail = await ttsResponse.text();
        console.error("Erreur ElevenLabs détaillée:", errorDetail);
        throw new Error("Erreur ElevenLabs");
    }

    const arrayBuffer = await ttsResponse.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    const audioBase64 = buffer.toString('base64');

    // 3. ON RENVOIE LE TEXTE + L'AUDIO
    res.json({ 
      reply: reply, 
      audio: `data:audio/mp3;base64,${audioBase64}` 
    });

  } catch (err) {
    console.error("Erreur générale:", err.message);
    res.status(500).json({ error: "Marie rencontre un problème technique." });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Serveur prêt sur le port ${PORT}`));