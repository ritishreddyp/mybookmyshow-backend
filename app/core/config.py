from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    PROJECT_NAME: str = "MyBookMyShow API"
    API_V1_STR: str = "/api/v1"

    #db_url
    DB_USER: str 
    DB_PASSWORD: str 
    DB_HOST: str 
    DB_PORT: int = 5432
    DB_NAME: str 


    #jwt
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    @property
    def db_url(self) -> str:

        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()