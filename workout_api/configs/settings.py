from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # Usa Field para mapear a variável de ambiente 'DATABASE_URL' para o campo 'DB_URL'
    DB_URL: str = Field(default='postgresql+asyncpg://workout:workout@localhost/workout', alias='DATABASE_URL')

settings = Settings()