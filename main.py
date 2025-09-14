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
    try:
        r = requests.post(f"{TEXT_PREP}/preprocess/text", json={"poem": payload["poem"]}, timeout=20)
        r.raise_for_status()
        text_meta = r.json()
    except Exception as e:
        text_meta = {"error": str(e)}
        logging.exception("Text preprocessing failed")

    # 2. image analysis (optional)
    image_embeddings = []
    if payload.get("images"):
        for img_uri in payload["images"]:
            try:
                r = requests.post(f"{IMAGE_ANALYSIS}/analyze/image", json={"uri": img_uri}, timeout=20)
                r.raise_for_status()
                image_embeddings.append(r.json())
            except Exception:
                logging.exception("Image analysis failed for %s", img_uri)

    # 3. lyrics generation
    try:
        r = requests.post(f"{LYRICS}/generate/lyrics", json={"poem": payload["poem"], "style": payload.get("style")}, timeout=30)
        r.raise_for_status()
        lyrics = r.json()
    except Exception as e:
        lyrics = {"error": str(e)}
        logging.exception("Lyrics generation failed")

    # 4. melody/harmony generation
    try:
        r = requests.post(f"{MELODY}/generate/melody", json={"lyrics": lyrics.get("verses") or [], "embedding": text_meta.get("embedding")}, timeout=60)
        r.raise_for_status()
        melody = r.json()
    except Exception as e:
        melody = {"error": str(e)}
        logging.exception("Melody generation failed")

    # 5. audio rendering
    try:
        r = requests.post(f"{RENDER}/render/audio", json={"lyrics": lyrics, "midi_url": melody.get("midi_url"), "style": payload.get("style")}, timeout=120)
        r.raise_for_status()
        audio = r.json()
    except Exception as e:
        audio = {"error": str(e)}
        logging.exception("Audio rendering failed")

    # 6. save metadata/history
    try:
        meta = {"job_id": job_id, "poem": payload["poem"], "style": payload.get("style"), "audio": audio.get("audio_url"), "midi": melody.get("midi_url")}
        requests.post(f"{HISTORY}/projects", json=meta, timeout=10)
    except Exception:
        logging.exception("Saving history failed")

    logging.info(f"Job {job_id} finished in {time.time()-start:.2f}s")