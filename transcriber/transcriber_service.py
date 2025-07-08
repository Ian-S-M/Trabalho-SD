from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import boto3
import uuid
import os
import time

app = FastAPI()

AWS_REGION = "us-east-1"
BUCKET_NAME = "bucketsdprojeto"  # Substituir pelo bucket real

# Clientes AWS
s3 = boto3.client("s3", region_name=AWS_REGION)
transcribe = boto3.client("transcribe", region_name=AWS_REGION)

def get_extension(filename, default="mp3"):
    if filename and "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    return default

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Gera nome único para o job e o arquivo
    job_name = f"job-{uuid.uuid4()}"
    audio_filename = f"{uuid.uuid4()}_{file.filename}"
    temp_path = f"/tmp/{audio_filename}"

    # Salva localmente
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Faz upload no S3
    try:
        s3.upload_file(temp_path, BUCKET_NAME, audio_filename)
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": f"Erro no upload para S3: {str(e)}"})

    # Extrai a extensão de forma segura
    media_format = get_extension(file.filename)

    # Inicia o job de transcrição
    media_uri = f"s3://{BUCKET_NAME}/{audio_filename}"
    try:
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": media_uri},
            MediaFormat=media_format,
            LanguageCode="pt-BR",
            OutputBucketName=BUCKET_NAME
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": f"Erro ao iniciar transcrição: {str(e)}"})

    # Espera terminar
    while True:
        job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = job["TranscriptionJob"]["TranscriptionJobStatus"]

        if status == "COMPLETED":
            transcript_uri = job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            break
        elif status == "FAILED":
            return JSONResponse(status_code=500, content={"erro": "Falha na transcrição"})
        time.sleep(5)

    # Baixa o resultado da transcrição
    import requests
    response = requests.get(transcript_uri)
    texto_transcrito = response.json()["results"]["transcripts"][0]["transcript"]

    return JSONResponse(content={"texto": texto_transcrito})