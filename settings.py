import pathlib
import logging.config

from logging import getLogger
from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).parent

# STORAGE
DB = dotenv_values(f'{BASE_DIR}/.env.postgres')
sqlalchemy_url = (f'postgresql+asyncpg://{DB["POSTGRES_USER"]}:{DB["POSTGRES_PASSWORD"]}@'
                  f'{DB["POSTGRES_HOST"]}:{DB["POSTGRES_PORT"]}/{DB["POSTGRES_DB"]}')

# LOGGING
log_file = f'{BASE_DIR}/log/error.log'


log_config = {
    'version': 1,
    'formatters': {
        'custom': {
            'format': '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'custom',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'custom',
            'filename': log_file,
            'maxBytes': 1024,
            'backupCount': 20,
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    },
}


def setup_logging():
    logging.config.dictConfig(log_config)
    logger = getLogger('app.settings')
    logger.info('Logging success initialized')