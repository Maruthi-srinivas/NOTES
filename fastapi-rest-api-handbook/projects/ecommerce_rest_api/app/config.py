from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://app:change-me@localhost:54329/ecommerce"
    test_database_url: str = "postgresql+asyncpg://app:change-me@localhost:54329/ecommerce_test"
    jwt_secret: str = "change-me-to-a-long-random-string"
    jwt_ttl_seconds: int = 3600
    admin_emails: str = "admin@example.com"

    @property
    def admin_email_set(self) -> set[str]:
        return {item.strip().lower() for item in self.admin_emails.split(",") if item.strip()}


settings = Settings()
