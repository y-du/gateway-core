"""
   Copyright 2020 Yann Dumont

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

__all__ = ("getLogger", )


from .configuration import gc_conf, user_dir
import logging.handlers
import os


logging_levels = {
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
    'debug': logging.DEBUG
}


class LoggerError(Exception):
    pass


msg_fmt = '%(asctime)s - %(levelname)s: [%(name)s] %(message)s'
date_fmt = '%m.%d.%Y %I:%M:%S %p'
standard_formatter = logging.Formatter(fmt=msg_fmt, datefmt=date_fmt)


stream_handler = logging.StreamHandler()
stream_handler.setFormatter(standard_formatter)


logger = logging.getLogger("gateway-core")
logger.propagate = False
logger.addHandler(stream_handler)


if gc_conf.Logger.level not in logging_levels.keys():
    err = "unknown log level '{}'".format(gc_conf.Logger.level)
    raise LoggerError(err)

if gc_conf.Logger.rotating_log:
    logger.removeHandler(stream_handler)
    logs_path = '{}/logs'.format(user_dir)
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    log_handler = logging.handlers.TimedRotatingFileHandler(
        '{}/gc.log'.format(logs_path),
        when="midnight",
        backupCount=gc_conf.Logger.rotating_log_backup_count
    )
    log_handler.setFormatter(standard_formatter)
    logger.addHandler(log_handler)

logger.setLevel(logging_levels[gc_conf.Logger.level])


def getLogger(name: str) -> logging.Logger:
    return logger.getChild(name)
