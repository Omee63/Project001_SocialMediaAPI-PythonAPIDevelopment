from pydantic.env_settings import BaseSettings


# This Pydantic BaseSetting extending class will perform validation and read all Environment variables.
# The Pydantic library for this case is case-insensitive.
# Note: we always read Environment Variables as String.
# Note: As per standard convention, we have to create '.env' file at the main directory
# which will contain all Environment Variables.
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_time_minutes: int

    # We are telling Pydantic to import ".env" file.
    class Config:
        env_file = ".env"


settings = Settings()
