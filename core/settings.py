from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    API_KEY: str
    API_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="API_",
        extra='ignore'
    )