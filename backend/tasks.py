# tasks.py
import os, uuid
from celery import Celery
from dotenv import load_dotenv
load_dotenv()
from db import SessionLocal, init_db, Job, Song
from lyrics_model import generate_lyrics
from music_model import generate_music_from_lyrics
from storage import save_file_from_path, save_bytes

CELERY_BROKER = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_BACKEND = os.getenv("CELERY_RESULT_BACKEND", CELERY_BROKER)
celery = Celery("tasks", broker=CELERY_BROKER, backend=CELERY_BACKEND)

init_db()

@celery.task(bind=True)
def generate_job(self, job_id: str, input_payload: dict):
    session = SessionLocal()
    try:
        # update job status
        session.query(Job).filter(Job.id == job_id).update({"status": "running"})
        session.commit()

        # 1) generate lyrics
        lyrics = generate_lyrics(input_payload.get("poemText",""), mood=input_payload.get("mood",""))

        # 2) music generation
        midi_path, audio_path = generate_music_from_lyrics(lyrics, mood=input_payload.get("mood",""),
                                                           ref_audio_path=input_payload.get("referenceAudioUrl"))

        # 3) upload outputs
        audio_url = save_file_from_path(audio_path, filename=f"{job_id}_song.mp3") if audio_path else None
        midi_url = save_file_from_path(midi_path, filename=f"{job_id}_song.mid") if midi_path else None

        # 4) write song record
        song_id = str(uuid.uuid4())
        song = Song(
            id=song_id,
            job_id=job_id,
            title=input_payload.get("poemTitle") or input_payload.get("title") or "Untitled",
            poem_title=input_payload.get("poemTitle"),
            poem_text=input_payload.get("poemText"),
            lyrics=lyrics,
            audio_url=audio_url,
            midi_url=midi_url,
            image_url=input_payload.get("imageUrl"),
            metadata={"mood": input_payload.get("mood")}
        )
        session.add(song)
        session.query(Job).filter(Job.id == job_id).update({"status": "completed"})
        session.commit()
        return {"status":"completed", "song_id": song_id}
    except Exception as e:
        session.query(Job).filter(Job.id == job_id).update({"status": "failed", "message": str(e)})
        session.commit()
        raise
    finally:
        session.close()