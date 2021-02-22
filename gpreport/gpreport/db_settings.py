import os
from typing import Optional
from pydantic import Field, BaseSettings
from dotenv import load_dotenv


class GlobalDBConfig(BaseSettings):
    """Global configurations."""

    # define global variables with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")
    # environment specific variables do not need the Field class
    HOST: Optional[str] = None
    PORT: Optional[int] = None
    DATABASE: Optional[str] = None
    CHARSET: Optional[str] = None
    USER: Optional[str] = None
    PASSWORD: Optional[str] = None

    class Config:

        """Loads the dotenv file."""

        from pathlib import Path  # Python 3.6+ only

        env_file = Path(".") / ".env"
        env_file_encoding = "utf-8"


class DevConfig(GlobalDBConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEV_"


class ProdConfig(GlobalDBConfig):
    """Production configurations."""

    class Config:
        env_prefix: str = "PROD_"


class StageConfig(GlobalDBConfig):
    """Staging configurations."""

    class Config:
        env_prefix: str = "STAGE_"


class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return DevConfig()

        elif self.env_state == "prod":
            return ProdConfig()

        elif self.env_state == "stage":
            return StageConfig()
