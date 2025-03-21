from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
import json
import asyncio
import time

from app.models.schemas import (
    CreateChatCompletionRequest,
    CreateChatCompletionResponse,
    CreateChatCompletionStreamResponse,
    ChatCompletionStreamResponseDelta,
    Object5 as Object,
    Choice2 as Choice,
    Role6 as Role,
    FinishReason1 as FinishReason

)

from app.core.security import get_api_key
from app.services.template_service import TemplateService
from app.services.token_service import TokenService

template_service = TemplateService()
token_service = TokenService()

router = APIRouter()

async def stream_chat_completion(tokens: list[str], response: CreateChatCompletionResponse):
    """Stream chat completion response in chunks"""
    # First chunk with role
    first_chunk = CreateChatCompletionStreamResponse(
        id=response.id,
        object=Object.chat_completion_chunk,
        created=int(time.time()),
        model=response.model,
        system_fingerprint=response.system_fingerprint,
        choices=[Choice(
            index=0,
            delta=ChatCompletionStreamResponseDelta(role=Role.assistant),
            finish_reason=None
        )]
    )
    yield {"data": json.dumps(first_chunk.model_dump())}
    
    # Stream each token with a small delay
    for i, token in enumerate(tokens):
        chunk = CreateChatCompletionStreamResponse(
            id=response.id,
            object=Object.chat_completion_chunk,
            created=int(time.time()),
            model=response.model,
            system_fingerprint=response.system_fingerprint,
            choices=[Choice(
                index=0,
                delta=ChatCompletionStreamResponseDelta(content=token),
                finish_reason=None
            )]
        )
        yield {"data": json.dumps(chunk.model_dump())}
    
    # Final chunk with finish reason
    final_chunk = CreateChatCompletionStreamResponse(
        id=response.id,
        object=Object.chat_completion_chunk,
        created=int(time.time()),
        model=response.model,
        system_fingerprint=response.system_fingerprint,
        choices=[Choice(
            index=0,
            delta=ChatCompletionStreamResponseDelta(),
            finish_reason=response.choices[0].finish_reason
        )]
    )
    yield {"data": json.dumps(final_chunk.model_dump())}
    yield {"data": "[DONE]"}

@router.post("/v1/chat/completions", response_model=CreateChatCompletionResponse)
async def create_chat_completion(
    request: CreateChatCompletionRequest,
    api_key: str = Depends(get_api_key)
):    
    # Get template response
    response_dict = template_service.render_template(
        "chat/completion.json.jinja"
    )

    response = CreateChatCompletionResponse(**response_dict)
    
    # Apply stop conditions
    content = response.choices[0].message.content
    
    # Check stop sequences
    if request.stop:
        stop_sequences = [request.stop] if isinstance(request.stop, str) else request.stop.root
        for sequence in stop_sequences:
            if sequence in content:
                content = content[:content.index(sequence)]
                response.choices[0].finish_reason = FinishReason.stop

    # Params depending on the tokenization
    if request.max_completion_tokens or request.stream:
        tokens = await token_service.tokenize(content)
    
        # Check max tokens
        if request.max_completion_tokens and request.max_completion_tokens < len(tokens):
            content = "".join(tokens[:request.max_completion_tokens])
            response.choices[0].finish_reason = FinishReason.length
        
        response.choices[0].message.content = content
    
        # Return streaming response if requested
        if request.stream:
            return EventSourceResponse(
                stream_chat_completion(tokens, response)
            )
    
    return response