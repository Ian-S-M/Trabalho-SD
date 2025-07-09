from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse, JSONResponse
import boto3
import io

app = FastAPI()   # <-- Certifique-se que o nome é app

app = FastAPI()

# Inicializa o cliente do Polly
polly = boto3.client('polly', region_name='us-east-2')

@app.post("/speak")

def speak(texto: str = Form(...)):
    
    # Gera um nome único para o arquivo
    
    audio_file = f"/tmp/{uuid.uuid4()}.mp3"

    # Requisição ao Polly
    
    response = polly.synthesize_speech(
        Text=texto,
        OutputFormat='mp3',
        VoiceId='Camila',  # voz feminina brasileira
        LanguageCode='pt-BR'
    )

    # Salva o áudio retornado
    
    with open(audio_file, 'wb') as f:
        
        f.write(response['AudioStream'].read())

    return FileResponse(path=audio_file, media_type="audio/mpeg", filename="resposta.mp3")