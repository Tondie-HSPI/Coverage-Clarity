from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Coverage Clarity API"
    app_env: str = "development"
    cors_allow_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_prefix="COVERAGE_CLARITY_")


settings = Settings()
