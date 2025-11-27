from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
    YamlConfigSettingsSource,
)

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

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
            A tuple containing the sources
            and their order for loading the settings values.
        """
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )

    bot_settings: BotSettings = BotSettings()
    parser_config: ParserConfig = ParserConfig()


settings = Settings()
