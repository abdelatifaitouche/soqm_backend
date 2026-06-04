from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    SUPER_USER_NAME: str
    SUPER_USER_LAST: str
    SUPER_USER_PWD: str
    SUPER_USER_EMAIL: str

    JWT_SECRET_KEY: str
    JWT_ALGO: str
    ACCESS_TOKEN_TIME: int  # hours
    REFRESH_TOKEN_TIME: int  # days

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
