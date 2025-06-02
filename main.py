from fastapi.responses import FileResponse
from database import *
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid

# Load environment variables from .env file
load_dotenv()

import requests
import time

base_url = "https://api.assemblyai.com"
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("ASSEMBLYAI_API_KEY environment variable is not set.")
headers = {
    "authorization": API_KEY
}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        file_contents = await file.read()
        
        # Create a temporary file to store the audio content
        temp_file_path = f"temp_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file_contents)
        
        with open(temp_file_path, "rb") as f:
            response = requests.post(base_url + "/v2/upload",headers=headers,data=f)
        audio_url = response.json()["upload_url"]
        data = {
            "audio_url": audio_url,
            "speech_model": "universal"
        }
        url = base_url + "/v2/transcript"
        response = requests.post(url, json=data, headers=headers)

        transcript_id = response.json()['id']
        polling_endpoint = base_url + "/v2/transcript/" + transcript_id

        while True:
            transcription_result = requests.get(polling_endpoint, headers=headers).json()
            transcript_text = transcription_result['text']

            if transcription_result['status'] == 'completed':
                print(f"Transcript Text:", transcript_text)
                break

            elif transcription_result['status'] == 'error':
                raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

            else:
                time.sleep(3)
        srt_response = requests.get(f"{polling_endpoint}/srt?chars_per_caption=32", headers=headers)
        with open(f"SRTDir/transcript_{transcript_id}.srt", "w") as srt_file:
            srt_file.write(srt_response.text)
        # Clean up the temporary file
        os.remove(temp_file_path)
        transcript = transcript_text
        
        # Save the transcript to the database
        db = next(get_db())
        new_transcript = Transcripts(id=transcript_id, fileName=file.filename, Transcript=transcript)
        db.add(new_transcript)
        db.commit()
        db.refresh(new_transcript)
        
        return {
            "id": str(new_transcript.id),
            "fileName": new_transcript.fileName,
            "transcript": new_transcript.Transcript
        }
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/export/{id}")
async def get_srt_file(id: str):
    file_path = f"SRTDir/transcript_{id}.srt"
    if not os.path.exists(file_path):
        return {"error": "SRT file not found"}
    return FileResponse(
        path=file_path,
        media_type='text/plain',
        filename=os.path.basename(file_path)
    )