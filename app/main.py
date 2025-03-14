from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import argparse
import uvicorn

from app.api.routes import chat
from app.core.config import settings
from app.middleware import RequestResponseLoggingMiddleware

app = FastAPI(title="Llama.Ipsum")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.enable_logs:
    app.add_middleware(RequestResponseLoggingMiddleware)

app.include_router(chat.router)

@app.get("/")
async def root():
    return {"message": "Llama.Ipsum is running"}

def parse_args():
    parser = argparse.ArgumentParser(description="OpenAI API Mock Server")
    parser.add_argument(
        "--host",
        help="Host to run the server on",
    )
    parser.add_argument(
        "--port",
        help="Port to run the server on",
    )
    parser.add_argument(
        "--template-dir", 
        help="Path to custom template directory"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    
    # TODO: Use Pydantic settings' CLI feature
    if args.template_dir:
        settings.template_dir = args.template_dir
    host = settings.host if args.host is None else args.host
    port = settings.port if args.port is None else args.port

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )

if __name__ == "__main__":
    main() 