from fastapi import FastAPI, File, UploadFile
import whisper
import os
import tempfile

app = FastAPI()
model = whisper.load_model("base")  # you can change to "small", "medium", etc.

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name

    result = model.transcribe(tmp_path)
    os.remove(tmp_path)
    return {"text": result["text"]}
