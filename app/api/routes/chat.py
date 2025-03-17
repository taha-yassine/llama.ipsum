from fastapi import APIRouter, Depends

from app.models.schemas import (
    CreateChatCompletionRequest,
    CreateChatCompletionResponse
)

from app.core.security import get_api_key
from app.services.template_service import TemplateService
from app.services.token_service import TokenService

template_service = TemplateService()
token_service = TokenService()

router = APIRouter()

@router.post("/v1/chat/completions", response_model=CreateChatCompletionResponse)
async def create_chat_completion(
    request: CreateChatCompletionRequest,
    api_key: str = Depends(get_api_key)
):    
    # Get template response
    response_dict = template_service.render_template(
        "chat/completion.json.jinja"
    )
    
    # Apply stop conditions
    content = response_dict["choices"][0]["message"]["content"]
    
    # Check stop sequences
    if request.stop:
        stop_sequences = [request.stop] if isinstance(request.stop, str) else request.stop.root
        for sequence in stop_sequences:
            if sequence in content:
                content = content[:content.index(sequence)]
                response_dict["choices"][0]["finish_reason"] = "stop"
    
    # Check max tokens
    if request.max_completion_tokens:
        truncated_content = await token_service.truncate_text(content, request.max_completion_tokens)
        if truncated_content != content:
            response_dict["choices"][0]["finish_reason"] = "length"
            content = truncated_content
    
    response_dict["choices"][0]["message"]["content"] = content
    return CreateChatCompletionResponse(**response_dict)