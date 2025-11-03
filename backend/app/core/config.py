import os

class Settings:
    PROJECT_NAME: str = "AI Verifier"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
