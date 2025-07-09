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

(Diagramas estão na pasta `assets/`)

---
## 🔒 Como o Grupo Garante a Segurança com AWS e Modelagem de Ameaça

A segurança dos dados é uma prioridade no nosso projeto. Por isso, escolhemos a AWS, que utiliza práticas avançadas de proteção, incluindo a **modelagem de ameaça**.

### O que é modelagem de ameaça?

Modelagem de ameaça é um processo contínuo usado pela AWS para identificar e analisar possíveis riscos de segurança nos sistemas e dados. Isso significa mapear tudo que pode ser alvo de ataques — como arquivos de áudio, transcrições e textos processados — e entender como proteger cada etapa do fluxo de informações.

### Como a AWS protege nossos dados?

- **Criptografia:**  
  Todos os dados do projeto são criptografados tanto em repouso (armazenados) quanto em trânsito (transferidos entre serviços). Podemos usar a criptografia padrão da AWS ou nossas próprias chaves.

- **Controle de acesso (IAM):**  
  Configuramos permissões para que apenas os serviços e usuários necessários tenham acesso aos recursos do projeto. Sempre seguimos o princípio do menor privilégio — ninguém acessa mais do que realmente precisa.

- **Registro e monitoramento:**  
  Todas as operações realizadas em nossos recursos ficam registradas no AWS CloudTrail. Assim, conseguimos auditar e detectar qualquer atividade suspeita.

- **Conformidade:**  
  A AWS possui certificações internacionais de segurança e privacidade, como ISO 27001, SOC, PCI-DSS e LGPD, o que nos dá confiança para utilizar os serviços em nosso projeto.

- **Isolamento de dados:**  
  Os dados do nosso projeto ficam isolados dos dados de outros clientes na AWS, garantindo mais segurança.

- **Avaliação contínua de ameaças:**  
  A AWS faz a modelagem de ameaça regularmente em todos os seus serviços, revisando e aprimorando as proteções para acompanhar novas vulnerabilidades.

### Como isso funciona no nosso projeto?

Quando um usuário envia um áudio para transcrição:
- O arquivo é criptografado assim que é salvo no S3.
- Apenas os serviços que autorizamos podem acessar esse arquivo.
- Todo o processo de transcrição e síntese acontece em ambientes seguros e isolados.
- Todas as operações ficam registradas para auditoria e acompanhamento posterior.

---

**Dica:**  
Nós recomendamos sempre ajustar as permissões IAM, ativar logs do CloudTrail e manter a criptografia habilitada, garantindo assim a máxima segurança dos dados de todos os usuários do sistema.

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
⚖️ Caso Real: Acessibilidade para Pessoa Surda em Tribunal
O Caso
Em setembro de 2020, o Tribunal Regional Federal da 4ª Região (TRF4), que abrange os estados do Sul do Brasil, promoveu uma audiência virtual que contou com a participação de uma parte surda. Para garantir a acessibilidade, o tribunal utilizou tecnologia de transcrição automática e intérpretes de Libras (Língua Brasileira de Sinais).

Como a tecnologia foi aplicada:

Durante a audiência, foi utilizada uma plataforma que convertia em tempo real o áudio das falas dos participantes em legendas automáticas, exibidas na tela.
A parte surda pôde acompanhar tudo por escrito, sem depender exclusivamente do intérprete, aumentando sua autonomia.
O sistema também permitiu que as falas escritas pela pessoa surda fossem lidas em voz alta por síntese de voz, facilitando a comunicação com os demais presentes.

Como nosso projeto poderia ser usado:

O nosso sistema, ao receber o áudio das falas dos participantes, transcreve automaticamente o conteúdo e ainda pode converter textos digitados em voz via Amazon Polly. Isso permite que uma pessoa surda:

Receba em tempo real a transcrição do que está sendo dito.
Escreva sua manifestação, que é convertida em áudio para todos ouvirem.
---

## 👥 Equipe

- Ian Soares Martins
  
- Gabriel Andrade Carvalho

- Alexandre Moraes Pereira Carvalhaes Filho

- Guilherme Resende Mendes da Silva

---

## 📚 Referências

- BRASIL. Lei nº 13.146, de 6 de julho de 2015. Estatuto da Pessoa com Deficiência.

- AWS Documentation – Amazon Transcribe

- AWS Documentation – Amazon Polly

- IBGE. Censo Demográfico 2022 – Características da população com deficiência auditiva.

