import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import json
import requests
import uuid

class BunqClient(object):

    def __init__(self, base="https://api.bunq.com/v1", secret=None):
        self.base, self.secret = base, secret.encode("latin1")
        self.headers = {}
        self.headers["Cache-Control"] = "no-cache"
        self.headers["User-Agent"] = "bunqclient 2017.7.8"
        self.headers["X-Bunq-Geolocation"] = "0 0 0 0 000"
        self.headers["X-Bunq-Language"] = "en_US"
        self.headers["X-Bunq-Region"] = "nl_NL"
        self.hierarchy = ["avatar", "attachment_public", "installation",
        "user", "user_person", "user_company", "device", "device_server",
        "session", "session_server", "server_public_key", "monetary_account",
        "monetary_account_bank", "payment", "payment_batch",
        "request_inquiry", "request_inquiry_batch", "request_response",
        "draft_payment", "schedule_payment", "schedule_payment_batch",
        "cash_register", "qr_code", "content", "schedule",
        "schedule_instance", "credential_password_ip", "ip",
        "tab_usage_single", "tab_usage_multiple", "tab", "tab_item",
        "tab_item_batch", "qr_code_content", "tab_result_inquiry",
        "tab_result_response", "mastercard_action", "token_qr_request_ideal",
        "card", "card_debit", "card_name", "chat", "chat_conversation",
        "message", "message_attachment", "message_text",
        "certificate_pinned", "attachment", "attachment_tab",
        "invoice", "customer_statement", "export_annual_overview", "content"]
        self.rsakey = RSA.generate(2048)
        self.signer = PKCS1_v1_5.new(self.rsakey) 
        installation = self.request(installation="", method="POST", data={
            "client_public_key": self.rsakey.publickey().exportKey().decode(
                'utf-8').replace("RSA PUBLIC KEY", "PUBLIC KEY")+"\n"})
        self.serverpublickey = installation["Response"][2]["ServerPublicKey"]
        self.token = installation["Response"][1]["Token"]["token"]
        self.headers["X-Bunq-Client-Authentication"] = self.token
        self.deviceserver = self.request(device_server="", method="POST", 
             data={"description": "bunqclient",
                   "secret": self.secret.decode('utf-8')})
        self.deviceserver = self.deviceserver["Response"][0]["Id"]["id"]
        self.session = self.request(session_server="", method="POST",
            data={"secret": self.secret.decode('utf-8')})
        self.token = self.session["Response"][1]["Token"]["token"]
        self.headers["X-Bunq-Client-Authentication"] = self.token
        return

    def request(self, method="GET", data="", **k):
        url = self.prepare(**k)
        if type(data) == type(dict()): data = json.dumps(data)
        self.headers["X-Bunq-Client-Request-Id"] = str(uuid.uuid4())
        if sorted(o.items())[0][1] != "installation":
            self.headers["X-Bunq-Client-Signature"] = self.sign(
                url[len(self.base)-3:], data, method).decode('utf-8')
        try: method = getattr(requests, method.lower())
        except AttributeError: method = requests.get
        return json.loads(method(url, data=data, headers=self.headers).text)

    def sign(self, url, data, method):
        signeddata = [" ".join([method, url])]
        for header, value in sorted(self.headers.items()):
            if (header in ['Cache-Control', 'User-Agent']) or (
                header[0:6] == "X-Bunq"):
                if header != "X-Bunq-Client-Signature":
                    signeddata.append(": ".join([header, value]))
        signeddata.extend(["", data])
        return base64.b64encode(self.signer.sign(SHA256.new().update(
            "\n".join(signeddata).encode("latin1"))))

    def prepare(self, **k):
        e = [self.base]
        o = {self.hierarchy.index(idtype): idtype for idtype in k.keys()}
        for _, i in sorted(o.items()): e.append("/".join([i, str(k[i])]))
        url = "/".join(e).replace("_", "-")
        return url[:-1] if url[-1] == "/" else url
