from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    app_name: str = "Expense Tracker"
    aws_region: str = "ap-south-1"
    log_level: str = "INFO"


settings = Settings()