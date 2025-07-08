# Sistema de Acessibilidade com Inteligência Artificial para Julgamentos

## 🎯 Objetivo

Este projeto tem como objetivo desenvolver um sistema distribuído com múltiplos agentes de inteligência artificial, voltado para auxiliar pessoas com deficiência auditiva em julgamentos, por meio de:

- Transcrição automática de falas (áudios) para texto com uso da AWS Transcribe;
  
- Leitura de textos gerados por IA com AWS Polly, facilitando o acompanhamento auditivo do conteúdo;
  
- Comunicação entre agentes via API, seguindo o modelo de microserviços.

---

## 🧩 Motivação do Problema

Pessoas com deficiência auditiva frequentemente enfrentam obstáculos em ambientes jurídicos devido à falta de recursos tecnológicos de acessibilidade. A ausência de transcrições automáticas e de leitura em tempo real compromete a participação plena e informada nesses ambientes.

Nosso sistema propõe um modelo que permite:

- Transcrição em tempo real de sessões;
  
- Leitura do conteúdo para acompanhantes, advogados ou intérpretes;
  
- Registro automático das falas em formato de texto e áudio.

---

## 🔗 Tecnologias Utilizadas

- **FastAPI** para APIs dos microserviços
 
- **AWS Transcribe** para transcrição automática
  
- **AWS Polly** para leitura de textos com voz natural
  
- **Python (3.10+)**
  
- **HTTP REST APIs** para comunicação entre agentes
  
- **GitHub** como controle de versão e rastreio de tarefas

---

## 🧠 Arquitetura do Sistema

- `transcriber_service`: recebe um áudio, envia para o AWS Transcribe, retorna o texto.
  
- `reader_service`: recebe o texto e retorna o áudio falado com AWS Polly.
  
- `api_gateway`: faz a orquestração entre os serviços e expõe a API principal para o usuário.

(Diagramas estão na pasta `docs/`)

---

## 📎 Estrutura de Diretórios

```bash

/acessibilidade-julgamento-ia/
  │ 
  ├── api_gateway/
  │     └── main.py
  │ 
  ├── transcriber/
  │     └── transcriber_service.py
  │ 
  ├── reader/
  │     └── reader_service.py
  │ 
  ├── docs/
  │     ├── arquitetura_inicial.png
  │     └── arquitetura_final.png
  │ 
  ├── README.md
  └── requirements.txt

```

---

## 🧪 Como Testar Localmente

```bash

# Instale as dependências

pip install -r requirements.txt

# Inicie os serviços separadamente

uvicorn transcriber.transcriber_service:app --reload
uvicorn reader.reader_service:app --reload
uvicorn api_gateway.main:app --reload

```

---

## 📚 Referências

- BRASIL. Lei nº 13.146, de 6 de julho de 2015. Estatuto da Pessoa com Deficiência.

- AWS Documentation – Amazon Transcribe

- AWS Documentation – Amazon Polly

- IBGE. Censo Demográfico 2022 – Características da população com deficiência auditiva.

---

## 👥 Equipe

- Ian Soares Martins
  
- Gabriel Andrade Carvalho

- Alexandre Moraes Pereira Carvalhaes Filho

- Guilherme Resende Mendes da Silva
