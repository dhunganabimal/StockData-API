from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOSTNAME:str
    # DB_PORT:int
    DB_PASSWORD:str
    DB_NAME:str
    DB_USERNAME:str


    model_config = {
        "env_file": ".env",
    }

settings=Settings()

