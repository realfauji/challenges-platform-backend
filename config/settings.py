from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URL:str
    DB_NAME:str
    
    ALGORITHM:str
    SECRET_KEY:str
    
    ACCESS_TOKEN:int
    REFRESH_TOKEN:int
    
    class Config():
        env_file = ".env"

settings = Settings()