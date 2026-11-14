import os
from dataclasses import dataclass
from pathlib import Path

# Optional light .env loading without external dependencies
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


@dataclass
class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Listing API")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./listings.db")


settings = Settings()
