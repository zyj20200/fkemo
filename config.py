import os
from dotenv import load_dotenv

load_dotenv()

class MysqlConfig:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "fkemo")


class Settings:
    DATABASE_URL = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        MysqlConfig.MYSQL_USER, MysqlConfig.MYSQL_PASSWORD, MysqlConfig.MYSQL_HOST, MysqlConfig.MYSQL_PORT,
        MysqlConfig.MYSQL_DATABASE)
    SECRET_KEY = "fkemo"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7   # 7 days


settings = Settings()