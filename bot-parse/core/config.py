from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class BotSettings(BaseModel):
    token: str = "token"  # noqa: S105


class ParserConfig(BaseModel):
    etp_gpb: str = (
        "https://etpgpb.ru/procedures.rss?page=1&per=100&procedure%5Bstage%5D%5B0%5D=accepting&search="
    )


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        case_sensitive=False,
        yaml_file=(
            BASE_DIR / "config.default.yaml",
            BASE_DIR / "config.local.yaml",
        ),
        yaml_config_section="bot",
    )

    bot_settings: BotSettings = BotSettings()
    parser_config: ParserConfig = ParserConfig()


settings = Settings()
