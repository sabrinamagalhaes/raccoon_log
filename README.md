# Log config

The main goals of this module are:

1. :pencil: **Standardize names**: create one file per day (append logs of the same day).

  * Follow the pattern **<name_passed_by_arg>_<current_day(%Y_%m_%d)>.log**, example: ```log_2016_06_10.log```

2. :bowtie: **Clean log directory**: compress old log files.

  * Settable using **compress**=[True|False]
  * Max number of not compressed files: **max_files_uncompressed**=N (N default 1)

3. :passport_control: **More control over the log**: create a new log level between WARNING and INFO, the **IMPORTANT** level.

  * As many downloader modules use INFO level to log requests (as GoogleAPI, Request,...), was created a new level, **IMPORTANT**, to use as INFO, but no so verbose.
  * Still can set the level: **max_level**=N (N the max level)

4. :e-mail: **Receive alerts**: receive SMS or Email alerts on ERROR/CRITICAL log or anything you want to know (optional).

  * Create a new log level between WARNING and ERROR, the **NOTIFY** level. If you want to receive alert of some action but it is not even ERROR or CRITICAL, just use `logging.notify()`
  * Uses [Plivo API](https://www.plivo.com/) to send SMS


## New level table:
| Level | Numeric value |
|:-----:|:-------------:|
|CRITICAL |	50 |
|ERROR	| 40 |
|**NOTIFY**	| **35** |
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

config_log(directory, log_name, max_files_uncompressed=1, max_level="IMPORTANT", compress=True, develop=False, send_email=True, to_emails=['example@gmail.com'], from_email='example@gmail.com', pwd='pwd_example', send_sms=True, to_phones=['5516111111111'], auth_id='EXAMPLEID', auth_token='EXAMPLETOKEN')
```

#### config_log arguments

> config_log(directory, log_name, max_files_uncompressed=1, max_level="IMPORTANT", compress=True, develop=False,
send_email=True, to_emails=['example@gmail.com'], from_email='example@gmail.com', pwd='pwd_example',
send_sms=True, to_phones=['5516111111111'], auth_id='EXAMPLEID', auth_token='EXAMPLETOKEN'
)

* **directory**: Directory to save the logs
* **log_name**: First part of the log name. The name will follow: "< NAME >_YEAR_MONTH_DAY.log"
* **max_files_uncompressed** (optional, default=1): number of uncompressed files
* **max_level** (optional, default='IMPORTANT'): max log level. Accept numbers (0 - 50)
* **compress** (optional, default=True) compress old log files to a .tar
* :new: **develop** (optional, default=False): set output from logging.important to standard ouput (normal print)
* :new: **send_email** (optional, default=False): boolean to activate or not alert by Email on CRITICAL, ERROR or NOTIFY level.
* **to_emails** (needed if send_email is True): list of emails to receive alerts.
* **from_email** (needed if send_email is True): email used to send email alert.
* **pwd** (needed if send_email is True): from_email password
* :new: **send_sms** (optional, default=False): boolean to receive or not alert by SMS on CRITICAL, ERROR or NOTIFY level.
* **to_phones** (needed if send_sms is True): list of phones to receive alerts. (Format: country code + ddd + number. Ex: 5516111111111)
* **auth_id** (needed if send_sms is True): auth id from Plivo
* **auth_token** (needed if send_sms is True): auth token from Plivo

### Use the log
In any child script
```python
import logging

logging.debug('Hello world!')
logging.important('This is important!')
logging.notify('An email was sent')
```
