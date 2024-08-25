from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str
    url_to_start_with: str
    output_dir: Path
    paths_to_exclude: list[str]


def get_settings() -> Settings:
    return Settings()
