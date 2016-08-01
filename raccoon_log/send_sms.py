import logging.handlers

from raccoon_notifier.sms_sender import SMSSender

from custom_levels import NOTIFY_LEVEL


class SendSMS(logging.handlers.BufferingHandler):

    def __init__(self, log_name, phones, auth_id, auth_token):
        """
        Initializes credentials to send SMS

        Args:
            log_name: first part of the log name;
            phones: list of phones to send to;
            auth_id: auth id from plivo;
            auth_token: auth token from plivo;
        """

        logging.handlers.BufferingHandler.__init__(self, 9999)
        self.log_name = log_name
        self.phones = phones
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.setLevel(NOTIFY_LEVEL)

    def flush(self):
        """
        Function to send log message via SMS

        """
        if len(self.buffer) == 0:
            return

        sender = SMSSender(self.log_name, self.auth_id, self.auth_token)
        msg = "\n".join(map(self.format, self.buffer))
        sender.send(self.phones, msg)
        self.buffer = []
