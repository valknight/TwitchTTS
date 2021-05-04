import logging
import os

me = logging.getLogger(__name__)
me.setLevel(logging.INFO)
level = logging.INFO

if bool(os.environ.get('DEBUG')):
    level = logging.DEBUG

logging.basicConfig(format='%(name)s:%(levelname)s:%(message)s', level=level)

if level == logging.DEBUG:
    me.info('debug mode enabled')


def get_logger(name) -> logging.Logger:
    l = logging.getLogger(name)
    return l
