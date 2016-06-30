# Log config

The main goals of this module are:

1. :pencil: **Standardize names**: create one file per day (append logs of the same day).

  * Follow the pattern **<name_passed_by_arg>_<current_day(%Y_%m_%d)>.log**, example: ```log_2016_06_10.log```

2. :bowtie: **Clean log directory**: compress old log files.

  * Settable using **compress**=[True|False]
  * Max number of not compressed files: **max_files_uncompressed**=N (N default 1)

3. :passport_control: **More control over the log**: create a new log level between WARNING and INFO, the **IMPORTANT** level.

  * As many downloader modules use INFO level to log requests (as GoogleAPI, Request,...), was created a new level, **IMPORTANT**, to use as INFO, but no so verbose.
  * Still can se the level: **max_level**=N (N the max level)


## New level table:
| Level | Numeric value |
|:-----:|:-------------:|
|CRITICAL |	50 |
|ERROR	| 40 |
|WARNING	| 30 |
|**IMPORTANT**	| **25** |
|INFO	| 20 |
|DEBUG	| 10 |
|NOTSET	| 0 |


## Usage

### Include repository

#### virtualenv
Include at ```requirements.txt```:
```python
git+https://github.com/devraccoon/raccoon_log
```
#### setup.py

```python
setup(
...
install_requires=[
...
'raccoon-log',
...
],
...
dependency_links=['https://github.com/devraccoon/raccoon_log/tarball/master#egg=raccoon-log'],
...
)
```

### Run the config
Run only in the main scipt
```python
from raccoon_log.config import config_log

config_log('/tmp/logs', 'example', max_files_uncompressed=2, max_level=25, compress=True)
```

#### config_log arguments

> config_log(directory, log_name, max_files_uncompressed=1, max_level="IMPORTANT", compress=True, develop=False)

* **directory**: Directory to save the logs
* **log_name**: First part of the log name. The name will follow: "< NAME >_YEAR_MONTH_DAY.log"
* **max_files_uncompressed**(optional, default=1) number of uncompressed files
* **max_level** (optional, default='IMPORTANT') max log level. Accept numbers (0 - 50)
* **compress** (optional, default=True) compress old log files to a .tar
* :new: **develop**: (optional, default=False) set output from logging.important to standard ouput (normal print)

### Use the log
In any child script
```python
import logging

logging.debug('Hello world!')
logging.important('This is important!')
```
