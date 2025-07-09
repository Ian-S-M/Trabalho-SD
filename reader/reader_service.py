from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
import boto3
import io

app = FastAPI()   # <-- Certifique-se que o nome é app

polly = boto3.client("polly", region_name="us-east-2")

@app.post("/speak")
async def speak(texto: str = Form(...)):
    try:
        response = polly.synthesize_speech(
            Text=texto,
            OutputFormat="mp3",
            VoiceId="Camila",
            LanguageCode="pt-BR"
        )
        audio_stream = response.get("AudioStream")
        if audio_stream:
            return StreamingResponse(io.BytesIO(audio_stream.read()), media_type="audio/mpeg")
        else:
            return JSONResponse(status_code=500, content={"erro": "Não foi possível obter o áudio."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})