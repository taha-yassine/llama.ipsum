from fastapi import HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models.schemas import Error1 as Error

API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Header(None, alias=API_KEY_NAME)):
    # Any API key should be valid
    # Only check if the header starts with Bearer
    # TODO: Implement proper API key validation
    if api_key_header and api_key_header.startswith("Bearer "):
        return api_key_header
    
    error = Error(
        type="invalid_request_error",
        message="You didn't provide an API key."
    )
    
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=error.model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )