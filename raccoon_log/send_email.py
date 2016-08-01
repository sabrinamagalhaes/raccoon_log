import logging.handlers

from raccoon_notifier.email_sender import EmailSender

from custom_levels import NOTIFY_LEVEL


class SendEmail(logging.handlers.BufferingHandler):

    def __init__(self, log_name, toaddrs, fromaddr, pwd):

        logging.handlers.BufferingHandler.__init__(self, 9999)
        self.log_name = log_name
        self.to_addrs = toaddrs
        self.from_addr = fromaddr
        self.pwd = pwd
        self.setLevel(NOTIFY_LEVEL)

    def flush(self):
        if len(self.buffer) == 0:
            return

        sender = EmailSender(self.log_name, self.from_addr, self.pwd)
        msg = "\n".join(map(self.format, self.buffer))
        sender.send(self.to_addrs, 'Attention: ' + self.log_name, msg)
        self.buffer = []
