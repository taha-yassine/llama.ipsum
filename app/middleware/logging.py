import json
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, StreamingResponse
from pathlib import Path
from starlette.background import BackgroundTask

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

def log_request_response(req_body: bytes, res_body: bytes):
    """Log request and response in the background"""
    try:
        request_data = json.loads(req_body) if req_body else None
    except Exception:
        request_data = req_body.decode() if req_body else None

    try:
        response_data = json.loads(res_body) if res_body else None
    except Exception:
        response_data = res_body.decode() if res_body else None

    log_entry = {
        "timestamp": logging.Formatter().formatTime(logging.LogRecord("", 0, "", 0, None, None, None)),
        "level": "INFO",
        "request": {
            "body": request_data
        },
        "response": {
            "body": response_data
        }
    }
    
    logger.info(log_entry)

class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Capture request body
        req_body = await request.body()
        
        # Get the original response
        response = await call_next(request)

        # No logging if streaming
        # TODO: support logging when streaming
        content_type = response.headers.get('content-type')
        if content_type and content_type.startswith('text/event-stream'):
            return response

        # Capture response body
        chunks = []
        async for chunk in response.body_iterator:
            chunks.append(chunk)
        res_body = b''.join(chunks)
        
        # Create background task for logging
        task = BackgroundTask(log_request_response, req_body, res_body)
        
        # Return new response with captured body and background logging
        return Response(
            content=res_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
            background=task
        )