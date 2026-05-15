from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "user"
    DB_PASS: str = "password"
    DB_NAME: str = "fastapi_db"

    @property
    def DATABASE_URL_async(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

model_config = SettingsConfigDict(env_file=".env")

settings = Settings()