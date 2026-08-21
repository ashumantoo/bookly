from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    # reading env variales from the .env file
    model_config = {"env_file": ".env", "extra": "ignore"}


Config = Settings()
