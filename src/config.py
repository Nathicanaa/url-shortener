import pydantic
import dotenv


class _Base(pydantic.BaseSettings):

    class Config:
        env_file = dotenv.find_dotenv(".env")


class PSQLConfig(_Base):
    psql_name: str
    psql_password: str
    psql_host: str
    psql_port: str | int
    database_name: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.psql_name}:{self.psql_password}@{self.psql_host}:{self.psql_port}/{self.database_name}"


class Config(pydantic.BaseSettings):
    db: PSQLConfig

