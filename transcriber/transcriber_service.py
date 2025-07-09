from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import boto3
import uuid
import os
import time
import tempfile
import traceback
import json


app = FastAPI()

AWS_REGION = "us-east-2"
BUCKET_NAME = "bucketsdprojeto"  # Troque pelo nome do seu bucket

# Clientes AWS

s3 = boto3.client("s3", region_name=AWS_REGION)
transcribe = boto3.client("transcribe", region_name=AWS_REGION)

def get_extension(filename, default="mp3"):
    
    if filename and "." in filename:
        
        return filename.rsplit(".", 1)[-1].lower()
        
    return default

@app.post("/transcribe")

async def transcribe_audio(audio: UploadFile = File(...)):
    
    try:
        
        print("Recebido arquivo:", audio.filename)
        # Nomes únicos para o job e arquivo
        job_name = f"job-{uuid.uuid4()}"
        audio_filename = f"{uuid.uuid4()}_{audio.filename}"
        print("Nome do job:", job_name)
        print("Nome do arquivo para S3:", audio_filename)

        # Salva temporariamente o arquivo
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{audio.filename}") as tmp:
            
            temp_path = tmp.name
            tmp.write(await audio.read())
            
        print("Arquivo temporário salvo em:", temp_path)

        # Upload para S3
        
        try:
            
            s3.upload_file(temp_path, BUCKET_NAME, audio_filename)
            print("Upload realizado com sucesso para S3.")
            
        except Exception as e:
            
            print("Erro no upload para S3:", str(e))
            return JSONResponse(status_code=500, content={"erro": f"Erro no upload para S3: {str(e)}"})

        # Descobre o formato do arquivo
        
        media_format = get_extension(audio.filename)
        print("Formato do arquivo:", media_format)

        # Inicia job de transcrição
        
        media_uri = f"s3://{BUCKET_NAME}/{audio_filename}"
        
        try:
            
            transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": media_uri},
                MediaFormat=media_format,
                LanguageCode="pt-BR",
                OutputBucketName=BUCKET_NAME
            )
            
            print("Job de transcrição iniciado.")
            
        except Exception as e:
            
            print("Erro ao iniciar transcrição:", str(e))
            return JSONResponse(status_code=500, content={"erro": f"Erro ao iniciar transcrição: {str(e)}"})

        # Aguarda job terminar
        
        while True:
            
            job = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = job["TranscriptionJob"]["TranscriptionJobStatus"]
            
            print("Status do job:", status)

            if status == "COMPLETED":
                
                transcript_uri = job["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
                
                print("Transcrição concluída. Transcript URI:", transcript_uri)
                
                break
                
            elif status == "FAILED":
                
                # DEBUG: imprime todo o retorno do job da AWS
                
                print("DETALHE DEBUG JOB:", job["TranscriptionJob"])
                
                failure_reason = job["TranscriptionJob"].get("FailureReason", "Motivo desconhecido")
                
                print("Falha na transcrição. Motivo:", failure_reason)
                
                return JSONResponse(status_code=500, content={"erro": f"Falha na transcrição: {failure_reason}"})
            time.sleep(5)

        # Baixa o resultado da transcrição USANDO BOTO3
        # transcript_uri exemplo: https://s3.us-east-2.amazonaws.com/bucketsdprojeto/job-xxxx.json
        # Remove o prefixo da URL para obter bucket e key
        
        s3_prefix = "https://s3.us-east-2.amazonaws.com/"
        
        if not transcript_uri.startswith(s3_prefix):
            
            return JSONResponse(status_code=500, content={"erro": "Formato inesperado do Transcript URI."})

        s3_uri = transcript_uri.replace(s3_prefix, "")
        bucket, key = s3_uri.split("/", 1)
        
        try:
            
            transcript_obj = s3.get_object(Bucket=bucket, Key=key)
            transcript_data = json.loads(transcript_obj['Body'].read())
            texto_transcrito = transcript_data["results"]["transcripts"][0]["transcript"]
            print("Texto transcrito obtido.")
            
        except Exception as e:
            
            print("Erro ao baixar/ler resultado da transcrição:", str(e))
            return JSONResponse(status_code=500, content={"erro": f"Erro ao obter resultado da transcrição: {str(e)}"})

        # Remove arquivo temporário
        
        try:
            
            os.remove(temp_path)
            print("Arquivo temporário removido.")
            
        except Exception as e:
            
            print("Não foi possível remover o arquivo temporário:", str(e))

        return JSONResponse(content={"texto": texto_transcrito})

    except Exception as e:
        
        print("Erro inesperado:", str(e))
        traceback.print_exc()
        
        return JSONResponse(status_code=500, content={"erro": f"Erro inesperado: {str(e)}"})
