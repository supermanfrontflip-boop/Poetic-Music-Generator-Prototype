from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import httpx
import os

app = FastAPI(title="Poetry-to-Music API Gateway")
docker-compose build
docker-compose up
TEXT_PRE_URL = os.getenv("TEXT_PRE_URL", "http://text_preprocessing:8000")
IMAGE_ANALYSIS_URL = os.getenv("IMAGE_ANALYSIS_URL", "http://image_analysis:8000")
LYRICS_URL = os.getenv("LYRICS_URL", "http://lyrics_generation:8000")
MELODY_URL = os.getenv("MELODY_URL", "http://melody_harmony:8000")
AUDIO_URL = os.getenv("AUDIO_URL", "http://audio_rendering:8000")

class PoemRequest(BaseModel):
    text: str
    mood: str = "calm"

@app.post("/generate")
async def generate_song(poem: PoemRequest, file: UploadFile = File(None)):
    async with httpx.AsyncClient() as client:
        # 1. Preprocess text
        pre = await client.post(f"{TEXT_PRE_URL}/preprocess/text", json={"text": poem.text})
        pre_data = pre.json()

        # 2. Image analysis (optional)
        captions = []
        if file:
            img_resp = await client.post(f"{IMAGE_ANALYSIS_URL}/analyze/image", files={"file": (file.filename, await file.read())})
            captions = img_resp.json().get("captions", [])

        # 3. Lyrics generation
        lyrics_input = {
            "theme": pre_data["summary"],
            "mood": poem.mood,
            "length": 150
        }
        lyr = await client.post(f"{LYRICS_URL}/generate/lyrics", json=lyrics_input)
        lyrics = lyr.json()["lyrics"]

        # 4. Melody generation
        mel = await client.post(f"{MELODY_URL}/generate/melody", json={"mood": poem.mood, "length": 16})
        midi_path = mel.json()["midi_path"]

        # 5. Audio rendering
        aud = await client.post(f"{AUDIO_URL}/render/audio", json={"midi_path": midi_path, "lyrics": lyrics})
        audio_path = aud.json()["audio_path"]

        return {
            "preprocessing": pre_data,
            "captions": captions,
            "lyrics": lyrics,
            "midi": midi_path,
            "audio": audio_path
        }
