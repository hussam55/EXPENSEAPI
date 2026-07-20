# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # This tells Pydantic to look for the .env file
    model_config = SettingsConfigDict(env_file=".env")

# Create a single instance of the settings to use across your whole app
settings = Settings()