from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil
from audio_converter import convert_to_8bit
from youtube_downloader import download_audio

app = FastAPI()

UPLOAD_DIR = "uploads/"
PROCESSED_DIR = "processed/"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "8bitify API is running!"}

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    output_path = os.path.join(PROCESSED_DIR, f"8bit_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    convert_to_8bit(file_path, output_path)
    
    return {"message": "File converted", "file_url": f"/processed/{file.filename}"}

@app.post("/youtube/")
async def youtube_to_8bit(url: str = Form(...)):
    try:
        file_path = download_audio(url)
        output_path = os.path.join(PROCESSED_DIR, f"8bit_{os.path.basename(file_path)}")
        convert_to_8bit(file_path, output_path)
        return {"message": "YouTube audio converted", "file_url": f"/processed/{os.path.basename(output_path)}"}
    except Exception as e:
        return {"error": str(e)}