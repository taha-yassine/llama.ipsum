from fastapi import APIRouter, Depends

from app.models.schemas import (
    CreateChatCompletionRequest,
    CreateChatCompletionResponse
)

from app.core.security import get_api_key
from app.services.template_service import TemplateService

template_service = TemplateService()

router = APIRouter()

@router.post("/v1/chat/completions", response_model=CreateChatCompletionResponse)
async def create_chat_completion(
    request: CreateChatCompletionRequest,
    api_key: str = Depends(get_api_key)
):    
    # Create response using template
    response_dict = template_service.render_template(
        "chat/chat.json.jinja"
    )

    # Convert to Pydantic model
    return CreateChatCompletionResponse(**response_dict)