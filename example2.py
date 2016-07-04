from raccoon_log.config import config_log
import logging

config_log('/tmp/logs', 'example', max_files_uncompressed=2, max_level='INFO', compress=True, develop=True)


logging.critical('Critical')
logging.error('Error')
logging.warning('Warning')
logging.important('Important')
logging.info('Info')
logging.debug('Debug')
