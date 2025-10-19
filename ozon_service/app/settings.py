from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    OZON_CLIENT_ID: str = os.getenv('OZON_CLIENT_ID')
    OZON_API_KEY: str = os.getenv('OZON_API_KEY')

    model_config = SettingsConfigDict(
        env_file='.env'
    )


settings = Settings()

if __name__ == '__main__':
    print(settings)