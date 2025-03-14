import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "api.log"

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, dict):
            return json.dumps(record.msg)
        return json.dumps({"message": record.getMessage()})

file_handler.setFormatter(JsonFormatter())

logger.addHandler(file_handler)

class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        await self._log_request(request)
        
        response = await call_next(request)
        
        await self._log_response(response)
        
        return response
    
    async def _log_request(self, request: Request):
        body = await self._get_request_body(request)
        
        log_entry = {
            "timestamp": logging.Formatter().formatTime(logging.LogRecord("", 0, "", 0, None, None, None)),
            "level": "INFO",
            "type": "request",
            "method": request.method,
            "path": request.url.path,
            "query_params": dict(request.query_params),
            "headers": dict(request.headers),
            "client": {"host": request.client.host if request.client else None},
            "body": body
        }
        
        logger.info(log_entry)
    
    async def _log_response(self, response: Response):
        log_entry = {
            "timestamp": logging.Formatter().formatTime(logging.LogRecord("", 0, "", 0, None, None, None)),
            "level": "INFO",
            "type": "response",
            "status_code": response.status_code,
            "headers": dict(response.headers)
        }
        
        # We can't easily log the response body as it's already been streamed
        # TODO: Implement proper response body logging
        
        logger.info(log_entry)
    
    async def _get_request_body(self, request: Request):
        # Save the request body position
        body_position = await request.body()
        
        # Reset the request body position for future middleware and endpoint
        request._body = body_position
        
        try:
            # Try to parse as JSON
            return json.loads(body_position)
        except Exception:
            # If not JSON, return as string
            return body_position.decode() if body_position else None 