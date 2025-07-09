from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import requests
import tempfile

app = FastAPI()

# URLs dos serviços
TRANSCRIBE_URL = "http://localhost:8001/transcribe"        # Porta do Transcriber
READER_URL = "http://localhost:8002/speak"                 # Porta do Reader

@app.post("/transcribe")
async def processar_audio(audio: UploadFile = File(...)):
    # Salva o áudio temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        
        tmp.write(await audio.read())
        audio_path = tmp.name

    # Envia para o serviço de transcrição
    with open(audio_path, "rb") as f:
        files = {"audio": (audio.filename, f, "audio/mpeg")}
        transcribe_response = requests.post(TRANSCRIBE_URL, files=files)

    if transcribe_response.status_code != 200:
        return JSONResponse(status_code=500, content={"erro": "Falha na transcrição"})

    texto_transcrito = transcribe_response.json().get("texto")
    if not texto_transcrito:
        return JSONResponse(status_code=500, content={"erro": "Transcrição vazia"})

    # Envia o texto para o serviço de leitura
    reader_response = requests.post(READER_URL, data={"texto": texto_transcrito})

    if reader_response.status_code != 200:
        return JSONResponse(status_code=500, content={"erro": "Falha na leitura de texto"})

    # Retorna tudo para o usuário
    return {
        "texto": texto_transcrito,
        "audio_mp3": reader_response.content.hex()[:100] + "..."  # preview do binário
    }