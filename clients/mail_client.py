import imaplib
import email
import email.utils
from settings import Settings


class MailClient:

    def __init__(self, settings: Settings):
        self.host = settings.mail_host
        self.user = settings.mail_user
        self.password = settings.mail_password
        self.mail = imaplib.IMAP4_SSL(self.host)

    def login(self):
        self.mail.login(self.user, self.password)

    def get_new_messages_in_folder(self, folder: str) -> dict:
        self.mail.select(folder)
        typ, data = self.mail.search(None, '(UNSEEN)')
        texts = {}
        for num in data[0].split():
            msg_datetime, text = self.read_message(num)
            if msg_datetime and text:
                texts[msg_datetime] = text
        return texts

    def get_messages_in_folder(self, folder: str) -> dict:
        self.mail.select(folder)
        typ, data = self.mail.search(None, 'ALL')
        texts = {}
        for num in data[0].split():
            msg_datetime, text = self.read_message(num)
            if msg_datetime and text:
                texts[msg_datetime] = text
        return texts

    def read_message(self, num):
        typ, data = self.mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        msg_datetime = email.utils.parsedate_to_datetime(msg.get('date'))
        text = self.decode_text_message(msg)
        return msg_datetime, text

    def decode_text_message(self, message):
        for part in message.walk():
            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                return part.get_payload(decode=True).decode()
