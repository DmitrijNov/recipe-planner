from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    API_KEY: str
    API_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="API_", extra="ignore"
    )


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "cookbook"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def url(self) -> str:
        """SQLAlchemy connection URL (psycopg3 driver, sync + async capable)."""
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


db_settings = DatabaseSettings()
