"""
Voice Copilot API Endpoints.
Provides multilingual natural language processing for farmer queries.
Connects directly to verified market prices, C2 cultivation benchmarks, and agronomic guidelines.
"""

import io
import logging
from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse

from crop_advisory.api.dependencies import get_voice_copilot_service, require_readiness
from crop_advisory.api.v1.schemas import (
    TextToSpeechRequest,
    VoiceQueryRequest,
    VoiceQueryResponse,
    VoiceTranscriptionResponse,
)
from crop_advisory.services.voice_copilot_service import VoiceCopilotService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["Kisan Voice Copilot"])


@router.post(
    "/query",
    response_model=VoiceQueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Process spoken or typed vernacular query",
    description="Parses farmer query in Marathi, Hindi, or English and returns verified responses from AGMARKNET and CACP.",
    dependencies=[Depends(require_readiness)],
)
async def process_voice_query(
    request: VoiceQueryRequest,
    copilot_service: VoiceCopilotService = Depends(get_voice_copilot_service),
) -> VoiceQueryResponse:
    """Processes farmer natural language question and generates verified audio/card response."""
    result = copilot_service.process_query(
        query_text=request.query_text,
        language=request.language,
        state=request.state,
    )
    return VoiceQueryResponse(**result)


@router.post(
    "/transcribe",
    response_model=VoiceTranscriptionResponse,
    status_code=status.HTTP_200_OK,
    summary="Transcribe spoken audio via Groq Whisper",
    description="Accepts microphone audio binary and transcribes into vernacular text without browser cloud dependencies.",
    dependencies=[Depends(require_readiness)],
)
async def transcribe_voice_audio(
    file: UploadFile = File(..., description="Recorded audio blob from browser MediaRecorder"),
    language: str = Query("mr", description="Language code ('mr', 'hi', 'en')"),
    copilot_service: VoiceCopilotService = Depends(get_voice_copilot_service),
) -> VoiceTranscriptionResponse:
    """Transcribes microphone audio using server-side Groq Whisper."""
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty audio recording submitted.",
        )

    filename = file.filename or "recording.webm"
    if not any(filename.endswith(ext) for ext in [".webm", ".wav", ".ogg", ".mp3", ".m4a"]):
        filename = f"{filename}.webm"

    content_type = file.content_type or "audio/webm"

    try:
        text = copilot_service.transcribe_audio(
            audio_bytes=audio_bytes,
            filename=filename,
            content_type=content_type,
            language=language,
        )
        return VoiceTranscriptionResponse(text=text, language=language, success=True)
    except Exception as e:
        logger.error("Audio transcription failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech transcription failed: {str(e)}",
        )


@router.post(
    "/speak",
    summary="Synthesize speech with ElevenLabs (Free Tier)",
    description="Converts spoken vernacular advice into high-quality ElevenLabs MP3 audio stream with quota caching.",
    dependencies=[Depends(require_readiness)],
)
async def synthesize_speech(
    request: TextToSpeechRequest,
    copilot_service: VoiceCopilotService = Depends(get_voice_copilot_service),
):
    """Streams ElevenLabs studio quality MP3 speech with quota-saving cache."""
    try:
        audio_bytes = copilot_service.synthesize_speech_elevenlabs(
            text=request.text,
            language=request.language,
        )
        return StreamingResponse(
            io.BytesIO(audio_bytes),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    except Exception as e:
        logger.error("Speech synthesis failed: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech synthesis failed: {str(e)}",
        )
