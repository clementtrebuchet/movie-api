class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///movie.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
