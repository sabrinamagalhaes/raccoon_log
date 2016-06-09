from log.configure import config_log

config_log('/tmp/logs', 'example', max_files_uncompressed=2, max_level=25, compress=True)
