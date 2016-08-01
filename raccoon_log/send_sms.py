import logging.handlers

from raccoon_notifier.sms_sender import SMSSender

from custom_levels import NOTIFY_LEVEL


class SendSMS(logging.handlers.BufferingHandler):

    def __init__(self, log_name, phones, auth_id, auth_token):

        logging.handlers.BufferingHandler.__init__(self, 9999)
        self.log_name = log_name
        self.phones = phones
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.setLevel(NOTIFY_LEVEL)

    def flush(self):
        if len(self.buffer) == 0:
            return

        sender = SMSSender(self.log_name, self.auth_id, self.auth_token)
        msg = "\n".join(map(self.format, self.buffer))
        sender.send(self.phones, msg)
        self.buffer = []
