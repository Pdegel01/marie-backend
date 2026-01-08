import express from "express";
import fetch from "node-fetch";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(cors());
app.use(express.json());

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const ELEVENLABS_API_KEY = process.env.ELEVENLABS_API_KEY; // Ta clé récupérée sur ElevenLabs

app.post("/chat", async (req, res) => {
  const { message, history } = req.body;

  if (!message) return res.status(400).json({ error: "Message vide" });

  try {
    // 1. APPEL À OPENAI POUR LE TEXTE (Ton code actuel)
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
            content: `Eres neoMarie, una profesora de français experta para hispanohablantes. 
            Tu estilo es directo, amable y muy conciso.
            REGLAS ESTRICTAS:
            1. Tus respuestas NO deben superar las 2 o 3 frases.
            2. Ve directamente al grano, sin introducciones largas.
            3. Explica brevemente en español y da el ejemplo en francés.
            4. Si el usuario te habla en español, respóndele brevemente para guiarlo al francés.` 
          },
          ...(history || []), 
          { role: "user", content: message }
        ],
        max_tokens: 150, 
        temperature: 0.7
      })
    });

    const data = await response.json();
    if (data.error) throw new Error(data.error.message);

    const reply = data.choices[0].message.content;

    // --- 2. NOUVEAU : APPEL À ELEVENLABS POUR LA VOIX (Rachel) ---
    const voiceId = "21m00Tcm4TlvDq8ikWAM"; // ID de la voix Rachel
    const ttsResponse = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}`, {
      method: "POST",
      headers: {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        text: reply,
        model_id: "eleven_multilingual_v2", // LE MODÈLE POUR LE BILINGUE FR/ES
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

    // On transforme le fichier audio binaire en texte Base64
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