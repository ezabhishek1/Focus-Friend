"""
Focus Friend - Extraction Endpoint Router.
Distills raw unstructured message text into Tone, Timeline, and Task.
Scalable synchronous handler automatically dispatched to worker threadpool.
"""

from fastapi import APIRouter, status
from backend.api.schemas.request_schemas import ExtractRequest
from backend.api.schemas.response_schemas import DistilledSignalResponse, ErrorResponse
from backend.services.extraction_service import ExtractionService

router = APIRouter(prefix="/extract", tags=["Distillation"])


@router.post(
    "",
    response_model=DistilledSignalResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input message or formatting."},
        500: {"model": ErrorResponse, "description": "Internal distillation failure."},
        503: {"model": ErrorResponse, "description": "Inference engine unavailable."},
        504: {"model": ErrorResponse, "description": "Inference timeout."},
    },
    summary="Distill raw text into Tone, Timeline, and Task"
)
def extract_signal(payload: ExtractRequest):
    """
    Distills walls of text into:
    - **The Vibe (Tone):** Plain-English emotional context to remove anxiety and rejection sensitivity.
    - **The Deadline (Timeline):** Target calendar dates and timeframes.
    - **The Action Item (Task):** A single imperative action point to kickstart execution.
    """
    result = ExtractionService.distill(text=payload.text, model=payload.model)
    return DistilledSignalResponse(**result)
