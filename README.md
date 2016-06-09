# Log config

Simple module to configure the logging module following a pattern.

### Usage
```python
from log.configure import config_log

#config_log(directory, log_name, max_files_uncompressed=1, max_level=25, compress=True):
config_log('/tmp/logs', 'example', max_files_uncompressed=2, max_level=25, compress=True)
```
