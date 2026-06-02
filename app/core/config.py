from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    aws_region: str

    class Config:
        env_file = ".env"

settings = Settings()