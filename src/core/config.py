from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    SUPER_USER_NAME: str
    SUPER_USER_LAST: str
    SUPER_USER_PWD: str
    SUPER_USER_EMAIL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
