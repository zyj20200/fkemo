class Settings:
    DATABASE_URL = "mysql+pymysql://root:123456@localhost/fkemo"
    SECRET_KEY = "mysecretkey"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()