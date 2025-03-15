from fastapi import APIRouter, Depends
from app.core.security import get_api_key
from app.models.schemas import (
    ListModelsResponse
)

from app.services.template_service import TemplateService

template_service = TemplateService()

router = APIRouter()

@router.get("/v1/models")
async def list_models(api_key: str = Depends(get_api_key)):
    """List available models"""
    response_dict = template_service.render_template(
        "models/list.json.jinja"
    )

    # Convert to Pydantic model
    return ListModelsResponse(
        object="list",
        data=response_dict
    )