from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    '''    DB_URL: str 
    SECRET_KEY_JWT: str 
    ALGORITHM: str
    MAIL_USERNAME: EmailStr 
    MAIL_PASSWORD: str
    MAIL_FROM: str 
    MAIL_PORT: int 
    MAIL_SERVER: str 
    REDIS_DOMAIN: str 
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = None
    CLD_NAME: str
    CLD_API_KEY: int
    CLD_API_SECRET: str'''
    DB_URL: str = os.getenv('DB_URL')
    SECRET_KEY_JWT: str = os.getenv('SECRET_KEY_JWT')
    ALGORITHM: str = os.getenv('ALGORITHM')
    MAIL_USERNAME: EmailStr = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD: str = os.getenv('MAIL_PASSWORD')
    MAIL_FROM: str = os.getenv('MAIL_FROM')
    MAIL_PORT: int = os.getenv('MAIL_PORT')
    MAIL_SERVER: str = os.getenv('MAIL_SERVER') 
    REDIS_DOMAIN: str = os.getenv('REDIS_DOMAIN') 
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = None
    CLD_NAME: str = os.getenv('CLD_NAME')
    CLD_API_KEY: int = os.getenv('CLD_API_KEY')
    CLD_API_SECRET: str = os.getenv('CLD_API_SECRET')

    @field_validator("ALGORITHM")
    @classmethod
    def validate_algorithm(cls, v):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v

    model_config = ConfigDict(extra="ignore", env_file = ".env", env_file_encoding = "utf-8")


config = Settings()