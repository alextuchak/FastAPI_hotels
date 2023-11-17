from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URL: str
    ACCESS_KEY: str
    SECRET_KEY: str
    MINIO_ENDPOINT: str
    MINIO_BUCKET: str

    model_config = SettingsConfigDict(env_file="app/.env", extra='ignore')


settings = Settings()
