from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator, RedisDsn


class Settings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"

    SYNC_SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SYNC_SQLALCHEMY_DATABASE_URI",  pre=True)
    def assemble_sync_db_connection(cls, v: Optional[str], values: Dict[str, Any]):
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    BOT_TOKEN: str

    class Config:
        case_sensitive = True


settings = Settings()
