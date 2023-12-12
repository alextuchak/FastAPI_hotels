from pydantic_settings import BaseSettings, SettingsConfigDict
import os
import yaml


yaml_settings = dict()
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'configs', 'images.yaml')) as f:
    yaml_settings.update(yaml.load(f, Loader=yaml.FullLoader))


class Settings(BaseSettings):
    MONGO_URL: str
    ACCESS_KEY: str
    SECRET_KEY: str
    MINIO_ENDPOINT: str
    MINIO_BUCKET: str
    IMAGES_SETTINGS: dict = yaml_settings['image_plugin']
    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str

    model_config = SettingsConfigDict(env_file="app/.env", extra='ignore')


settings = Settings()
