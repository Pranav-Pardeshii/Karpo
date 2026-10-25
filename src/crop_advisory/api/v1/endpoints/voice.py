"""
Voice Copilot API Endpoints.
Provides multilingual natural language processing for farmer queries.
Connects directly to verified market prices, C2 cultivation benchmarks, and agronomic guidelines.
"""

import logging
from fastapi import APIRouter, Depends, status

from crop_advisory.api.dependencies import get_voice_copilot_service, require_readiness
from crop_advisory.api.v1.schemas import VoiceQueryRequest, VoiceQueryResponse
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
