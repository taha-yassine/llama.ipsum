import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):    
    # Server settings
    host: str = os.environ.get("LLAMA_IPSUM_HOST", "localhost")
    port: int = os.environ.get("LLAMA_IPSUM_PORT", 8000)
    
    # Template settings
    template_dir: str = os.environ.get("LLAMA_IPSUM_TEMPLATE_DIR", "")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="LLAMA_IPSUM_"
    )

settings = Settings()