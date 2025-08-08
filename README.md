# Morning Brief Voice Agent

## Overview

A sophisticated voice-enabled AI assistant that runs on Telegram, providing intelligent daily email and calendar summaries through voice interaction. The system integrates with Microsoft Outlook, processes voice messages through an AI Agent with multiple tools, and responds with both text and voice outputs.

## Features

- 🎤 **Voice Input Processing**: Accepts voice messages via Telegram
- 🔊 **Voice Output**: Responds with synthesized speech 
- 🧠 **AI Agent Integration**: Groq Chat Model with Simple Memory
- 📧 **Real Outlook Integration**: Fetches actual emails and calendar events
- 📊 **Multiple Data Sources**: Microsoft Outlook (messages, calendar, events)
- 🤖 **Intelligent Processing**: AI-powered summary generation with context awareness
- 🐳 **Containerized**: All services running in Docker
- 🛡️ **Error Handling**: Robust retry logic and fallback responses

## Architecture

```
┌─ Telegram Voice Input ─┐
│                        │
▼                        │
ASR (Whisper)           │
│                        │
▼                        │
n8n Workflow Engine     │
├── AI Agent (Groq)     │
├── Simple Memory       │
├── Microsoft Outlook 1 │
├── Microsoft Outlook 2 │
└── Microsoft Outlook 3 │
│                        │
▼                        │
TTS (OpenTTS)           │
│                        │
▼                        │
└─ Telegram Voice Output ┘
```

## Prerequisites

- Docker and Docker Compose
- Telegram Bot Token
- Windows/Linux/Mac environment

## Quick Start

### 1. Clone Repository
```bash
git clone <repository-url>
cd morning-brief-agent
```

### 2. Start Services
```bash
# Start core services
docker run -d --name whisper-asr -p 8002:8000 whisper-asr:latest
docker run -d --name synesthesiam-opentts -p 5500:5500 synesthesiam/opentts:en
docker run -d --name n8n -p 5555:5678 n8nio/n8n:latest

# Create network and connect services
docker network create morning-brief-network
docker network connect morning-brief-network whisper-asr
docker network connect morning-brief-network synesthesiam-opentts
docker network connect morning-brief-network n8n
```

### 4. Configure n8n Workflow
1. Open `http://localhost:5555`
2. Login with credentials
3. Import workflow from `n8n/workflows/morning-brief.json`
4. Activate workflow

### 5. Test System
Send voice message saying "start summary" to your Telegram bot.

## Service Configuration

### ASR Service (Whisper)
- **Port**: 8002
- **Endpoint**: `/transcribe`
- **Input**: Audio file data
- **Output**: Transcribed text

### TTS Service (OpenTTS)
- **Port**: 5500
- **Endpoint**: `/api/tts`
- **Parameters**: `voice`, `text`
- **Output**: Audio file (WAV/OGG)

### n8n Workflow Engine
- **Port**: 5555
- **Interface**: Web-based workflow editor
- **Authentication**: Basic auth (see .env)

## Workflow Components

### 1. Voice Input Validation
```javascript
const validationSchema = {
    file_id: "string",
    file_path: "string", 
    file_size: "number",
    file_extension: "oga|mp3|wav|m4a"
};
```

### 2. Trigger Detection
- Listens for "start summary" phrase
- Routes to summary generation

### 2. Summary Generation with AI Agent
- **AI Model**: Groq Chat Model for intelligent processing
- **Memory**: Simple Memory for conversation context
- **Data Sources**: Real Microsoft Outlook integration
  - **Outlook 1**: Unread messages
  - **Outlook 2**: Calendar events  
  - **Outlook 3**: Additional Outlook data
- **Processing**: AI-powered natural language generation

### 4. Voice Synthesis
- Converts text summary to speech
- Uses OpenTTS with English voice models
- Returns audio in compatible format

## Error Handling

### Retry Logic
- **Max Retries**: 3 attempts
- **Backoff**: 1000ms between retries
- **Scope**: HTTP requests to ASR/TTS services

## API Endpoints

### Health Checks
```bash
# Check service status
curl http://localhost:8002/health  # ASR (may return 404 - normal)
curl http://localhost:5500/api/tts?text=test  # TTS
curl http://localhost:5555  # n8n
```

### Manual Testing
```bash
# Test ASR
curl -X POST http://localhost:8002/transcribe \
  -H "Content-Type: application/json" \
  -d '{"audio_data": "base64_data"}'

# Test TTS  
curl "http://localhost:5500/api/tts?voice=coqui-tts:en_vctk%23p229&text=Hello"
```

## Troubleshooting

### Common Issues

**1. Services Not Responding**
```bash
# Check container status
docker ps

# Restart services
docker restart whisper-asr synesthesiam-opentts n8n
```

**2. Network Connectivity**
```bash
# Verify network setup
docker network inspect morning-brief-network

# Test inter-service communication
docker exec n8n curl http://whisper-asr:8000/health
```

### Logs
```bash
# View service logs
docker logs whisper-asr --tail 50
docker logs synesthesiam-opentts --tail 50
docker logs n8n --tail 50
```




