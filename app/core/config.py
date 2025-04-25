# Core config and settings
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "OpenElections KE"
    debug: bool = True

settings = Settings()
