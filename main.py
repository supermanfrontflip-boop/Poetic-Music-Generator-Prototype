from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import requests, uuid, os, logging, time

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="API Gateway")

TEXT_PREP = os.getenv("TEXT_PREP_URL", "http://text_preprocessing:8000")
IMAGE_ANALYSIS = os.getenv("IMAGE_ANALYSIS_URL", "http://image_analysis:8000")
LYRICS = os.getenv("LYRICS_URL", "http://lyrics_generation:8000")
MELODY = os.getenv("MELODY_URL", "http://melody_harmony:8000")
RENDER = os.getenv("RENDER_URL", "http://audio_rendering:8000")
STORAGE = os.getenv("STORAGE_URL", "http://storage:8000")
HISTORY = os.getenv("HISTORY_URL", "http://history_metadata:8000")

class GenerateRequest(BaseModel):
    poem: str
    style: str | None = None
    images: list[str] | None = None
    options: dict | None = None

@app.post("/generate", status_code=202)
async def generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    background_tasks.add_task(orchestrate_job, job_id, req.dict())
    return {"job_id": job_id, "status": "queued"}

def orchestrate_job(job_id: str, payload: dict):
    logging.info(f"Job {job_id} started")
    start = time.time()
    # 1. text preprocessing
    from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Text Preprocessing Service")

# Load Hugging Face sentiment + keyword pipeline
sentiment_analyzer = pipeline("sentiment-analysis")
summarizer = pipeline("summarization")

class TextRequest(BaseModel):
    text: str

@app.post("/preprocess/text")
async def preprocess_text(req: TextRequest):
    sentiment = sentiment_analyzer(req.text[:512])[0]
    summary = summarizer(req.text[:512], max_length=60, min_length=20, do_sample=False)[0]["summary_text"]

    return {
        "tokens": req.text.split(),
        "sentiment": sentiment,
        "summary": summary
    }

    # 2. image analysis (optional)
    from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
from PIL import Image

app = FastAPI(title="Image Analysis Service")

# Hugging Face image-to-text model
captioner = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

@app.post("/analyze/image")
async def analyze_image(file: UploadFile = File(...)):
    image = Image.open(file.file)
    captions = captioner(image)

    return {
        "captions": [c["generated_text"] for c in captions]
    }

    # 3. lyrics generation
    from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Lyrics Generation Service")

# Hugging Face GPT-2 fine-tuned for lyrics/poetry
generator = pipeline("text-generation", model="gpt-2")

class LyricsRequest(BaseModel):
    theme: str
    mood: str
    length: int = 100

@app.post("/generate/lyrics")
async def generate_lyrics(req: LyricsRequest):
    prompt = f"Write a {req.mood} song about {req.theme}:"
    lyrics = generator(prompt, max_length=req.length, num_return_sequences=1, do_sample=True)[0]["generated_text"]

    return {"lyrics": lyrics}

    # 4. melody/harmony generation
    from fastapi import FastAPI
from pydantic import BaseModel
import pretty_midi
import random

app = FastAPI(title="Melody & Harmony Service")

class MelodyRequest(BaseModel):
    mood: str
    length: int = 16  # measures

@app.post("/generate/melody")
async def generate_melody(req: MelodyRequest):
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    # Simple scale mapping
    scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C major

    for i in range(req.length):
        note = random.choice(scale)
        note_obj = pretty_midi.Note(
            velocity=100,
            pitch=note,
            start=i * 0.5,
            end=(i + 1) * 0.5
        )
        piano.notes.append(note_obj)

    midi.instruments.append(piano)
    midi_path = "/tmp/melody.mid"
    midi.write(midi_path)

    return {"midi_path": midi_path}

    # 5. audio rendering
    from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI(title="Audio Rendering Service")

class RenderRequest(BaseModel):
    midi_path: str
    lyrics: str = ""

@app.post("/render/audio")
async def render_audio(req: RenderRequest):
    # FluidSynth must be installed in container
    output_path = "/tmp/output.wav"
    subprocess.run([
        "fluidsynth", "-ni", "example.sf2", req.midi_path, "-F", output_path, "-r", "44100"
    ])

    return {"audio_path": output_path}

    # 6. save metadata/history
    try:
        meta = {"job_id": job_id, "poem": payload["poem"], "style": payload.get("style"), "audio": audio.get("audio_url"), "midi": melody.get("midi_url")}
        requests.post(f"{HISTORY}/projects", json=meta, timeout=10)
    except Exception:
        logging.exception("Saving history failed")

    logging.info(f"Job {job_id} finished in {time.time()-start:.2f}s")
