import os
import sys
from contextlib import contextmanager


from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ConfigService import ConfigService

config = ConfigService()


engine = create_engine(
    config.get_database_url(),
    pool_size=10,
    max_overflow=30
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def config_logger(name: str):
    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True)
    logger.add(config.get_logs_dir() + name + "_info_{time}.log", rotation="1 week", level="INFO", colorize=True)
    logger.add(config.get_logs_dir() + name + "_debug_{time}.log", rotation="1 week", level="DEBUG",
               backtrace=True,
               diagnose=True)
    return logger


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# if not os.path.exists(config.get_temp_dir()):
#     os.makedirs(config.get_temp_dir())
#     logger.info("temp dir created")


def bootstrap(name: str = 'api'):
    # openai.api_key = config.get_openai_token()
    # openai.api_base = config.get_helicone_url() or openai.api_base
    # #Base.metadata.create_all(bind=engine)
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = config.get_openai_token()
    # config_logger(name)
