import logging
import logging.handlers
import tarfile
from datetime import datetime
from os import listdir
from os import makedirs
from os import path
from os import remove
from os.path import isfile, join

from custom_levels import IMPORTANT_LEVEL, important, notify, NOTIFY_LEVEL
from send_email import SendEmail
from send_sms import SendSMS


def _to_path(value):
    """
    Return the value stripped.

    Args:
        value: string to strip;
    Return:
        string: stripped string;
    """
    value = value.lstrip()
    value = value.rstrip(' /')
    value += '/'
    return value


def _get_log_level(max_level):
    """
    Get log level based at max_level argument (accept number or string).

    Args:
        max_level: max level of log;
    """
    log_level = IMPORTANT_LEVEL
    if max_level:
        if isinstance(max_level, int):
            log_level = max_level
        elif max_level.isdigit():
            log_level = int(max_level)
        elif max_level == 'CRITICAL':
            log_level = 50
        elif max_level == 'ERROR':
            log_level = 40
        elif max_level == 'NOTIFY':
            log_level = NOTIFY_LEVEL
        elif max_level == 'WARNING':
            log_level = 30
        elif max_level == 'IMPORTANT':
            log_level = IMPORTANT_LEVEL
        elif max_level == 'INFO':
            log_level = 20
        elif max_level == 'DEBUG':
            log_level = 10
        elif max_level == 'NOTSET':
            log_level = 0
    return log_level


def config_log(directory, log_name, max_files_uncompressed=1, max_level="IMPORTANT", compress=True, develop=False,
               send_email=False, to_emails=None, from_email=None, pwd=None,
               send_sms=False, to_phones=None, auth_id=None, auth_token=None):
    """
    Configure log using a default pattern and create a new level (important).

    Args:
        directory: folder to save logs;
        log_name: first part of the log name;
        max_files_uncompressed: max number of remaining not compressed files;
        max_level: max level of log;
        compress: indicates if compress the logs or no;
        develop: set output from logging.important to standard ouput (normal print);
        send_email: boolean to activate or not alert by Email on CRITICAL, ERROR or NOTIFY leve.;
        to_emails (needed if send_email is True): list of emails to receive alert;
        from_email (needed if send_email is True): email used to send email alert;
        pwd (needed if send_email is True): from_email password;
        send_sms: boolean to receive or not alert by SMS on CRITICAL, ERROR or NOTIFY level;
        to_phones (needed if send_sms is True): list of phones to receive alert ;
        auth_id (needed if send_sms is True): auth id from Plivo;
        auth_token (needed if send_sms is True): auth token from Plivo;
    """
    end_with = '.log'
    directory = _to_path(directory)

    if not path.exists(directory):
        makedirs(directory)

    email_handler = None
    sms_handler = None
    if send_email:
        email_handler = SendEmail(log_name, to_emails, from_email, pwd)

    if send_sms:
        sms_handler = SendSMS(log_name, to_phones, auth_id, auth_token)

    _set_logger(directory, log_name, _get_log_level(max_level), develop, email_handler, sms_handler)

    if compress and not develop:
        _clean_up_logs(directory, log_name, end_with, max_files_uncompressed)


def _set_logger(directory, name, level, develop, email_handler, sms_handler):
    """
    Set the log pattern using default configs.

    Args:
        directory: folder to save the log;
        name: name of the software;
        level: log level;
        develop: enable to use print instead of log;
        email_handler: email handler to add to log
        sms_handler: sms handler to add to log
    """
    now = datetime.now().strftime('%Y_%m_%d')
    log_path = '{}/{}_{}.log'.format(directory, name, now)

    format_pattern = '[%(asctime)s.%(msecs)d] - %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    if develop:
        logging.basicConfig(format=format_pattern, datefmt=date_format, level=level)
    else:
        logging.basicConfig(filename=log_path, filemode='a', format=format_pattern, datefmt=date_format, level=level)

    logging.important = important
    logging.notify = notify

    if email_handler:
        logging.root.addHandler(email_handler)
    if sms_handler:
        logging.root.addHandler(sms_handler)


def _clean_up_logs(directory, starts_with, ends_with, max_files_uncompressed):
    """
    Compress old logs as a '.tar' file.

    Args:
        directory: folder to save the log;
        starts_with: first part of the name used at log files;
        ends_with: extension of log files;
        max_files_uncompressed: max number of remaining not compressed files;
    """
    log_files = [log_file for log_file in listdir(directory) if isfile(join(directory, log_file)) and
                 log_file.startswith(starts_with) and log_file.endswith(ends_with)]

    if max_files_uncompressed < 1:
        return

    if log_files and len(log_files) > max_files_uncompressed:
        log_files.sort()
        [log_files.pop() for _ in range(max_files_uncompressed)]

        compressed_name = '{}_logs'.format(starts_with)
        tar_path = '{}/{}.tar'.format(directory, compressed_name)

        tar_stream = tarfile.open(tar_path, mode='a')
        try:
            for log_file in log_files:
                log_file_path = '{}/{}'.format(directory, log_file)
                tar_stream.add(log_file_path, arcname=log_file)
                remove(log_file_path)
        except Exception as err:
            logging.important('Error compressing logs. (Error: {0})'.format(err))
        tar_stream.close()
