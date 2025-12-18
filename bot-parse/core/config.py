from pathlib import Path
from enum import Enum

from pydantic import BaseModel, HttpUrl
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

BASE_DIR = Path(__file__).resolve().parent.parent


class KeyWord(Enum):
    grav: str = "Гравим"
    electro: str = "Электроразв"
    magnit: str = "Магниторазв"
    geodin: str = "Геодинам"


class ParserConfig(BaseModel):
    etp_gpb: HttpUrl = (
        "https://etpgpb.ru/procedures.rss?page=1&per=100&procedure%5Bstage%5D%5B0%5D=accepting&search="
    )

    lukhoil: HttpUrl = (
        "https://lukoil.ru/Company/Tendersandauctions/Tenders/TendersofLukoilgroup?tab=1&organization=0&country=0"
    )

    tek_torg: HttpUrl = "https://www.tektorg.ru/procedures?name="
    sber: HttpUrl = r"https://www.sberbank-ast.ru/Default.aspx"


class SessionHeaders(BaseModel):
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(
            BASE_DIR / ".env.example",
            BASE_DIR / ".env",
        ),
        env_prefix="BOT__",
        env_nested_delimiter="_",
    )

    token: str
    parser_config: ParserConfig = ParserConfig()
    session_header: SessionHeaders = SessionHeaders()


settings = Settings()
