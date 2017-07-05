import base64
import Crypto.Hash.SHA256
import Crypto.PublicKey.RSA
import Crypto.Signature.PKCS1_v1_5
import json
import requests
import uuid

class BunqClient(object):

    def __init__(self,
                 base="https://api.bunq.com/v1",
                 secret=None,
                 **kwargs):
        self.base = base
        self.secret = secret.encode("latin1")
        self.headers = {}
        self.headers["Cache-Control"] = "no-cache"
        self.headers["User-Agent"] = "bunqclient 2017.7.7"
        self.headers["X-Bunq-Geolocation"] = "0 0 0 0 000"
        self.headers["X-Bunq-Language"] = "en_US"
        self.headers["X-Bunq-Region"] = "nl_NL"
        self.hierarchy = ["avatar", "attachment-public", "installation",
        "user", "user-person", "user-company", "device", "device-server",
        "session", "session-server", "server-public-key", "monetary-account",
        "monetary-account-bank", "payment", "payment-batch",
        "request-inquiry", "request-inquiry-batch", "request-response",
        "draft-payment", "schedule-payment", "schedule-payment-batch",
        "cash-register", "qr-code", "content", "schedule",
        "schedule-instance", "credential-password-ip", "ip",
        "tab-usage-single", "tab-usage-multiple", "tab", "tab-item",
        "tab-item-batch", "qr-code-content", "tab-result-inquiry",
        "tab-result-response", "mastercard-action", "token-qr-request-ideal",
        "card", "card-debit", "card-name", "chat", "chat-conversation",
        "message", "message-attachment", "message-text",
        "certificate-pinned", "attachment", "attachment-tab",
        "invoice", "customer-statement", "export-annual-overview", "content"]
        self.rsakey = Crypto.PublicKey.RSA.generate(2048)
        self.signer = Crypto.Signature.PKCS1_v1_5.new(self.rsakey) 
        installation = self.request(
            'installation', method="POST", 
            data={"client_public_key": 
                  self.rsakey.publickey().exportKey().decode('utf-8').replace(
                    "RSA PUBLIC KEY", "PUBLIC KEY")+"\n"})
        self.serverpublickey = installation["Response"][2]["ServerPublicKey"]
        self.token = installation["Response"][1]["Token"]["token"]
        self.headers["X-Bunq-Client-Authentication"] = self.token
        self.deviceserver = self.request(
            'device-server',
            method="POST",
            data={"description": "bunqclient",
                  "secret": self.secret.decode('utf-8')})
        self.deviceserver = self.deviceserver["Response"][0]["Id"]["id"]
        self.session = self.request(
            'session-server',
            method="POST",
            data={"secret": self.secret.decode('utf-8')})
        self.token = self.session["Response"][1]["Token"]["token"]
        self.headers["X-Bunq-Client-Authentication"] = self.token
        return

    def request(self, method="GET", data="", **k):
        o = {self.hierarchy.index(idtype): idtype for idtype in k.keys()}
        e = [self.base, request]
        e.extend(["/".join([i.replace("_", "-"), 
                            str(j)]) for i, j in sorted(o.items())])
        url = "/".join(e)
        if type(data) == type(dict()): data = json.dumps(data)
        self.headers["X-Bunq-Client-Request-Id"] = str(uuid.uuid4())
        if request != "installation":
            self.headers["X-Bunq-Client-Signature"] = self.sign(
                url[len(self.base)-3:], data, method).decode('utf-8')
        try: method = getattr(requests, method.lower())
        except AttributeError: method = requests.get
        return json.loads(method(url, data=data, headers=self.headers).text)

    def sign(self, url, data, method):
        signeddata = []
        signeddata.append(" ".join([method, url]))
        for header, value in sorted(self.headers.items()):
            if (header in ['Cache-Control', 'User-Agent']) or (
                header[0:6] == "X-Bunq"):
                if header != "X-Bunq-Client-Signature":
                    signeddata.append(": ".join([header, value]))
        signeddata.extend(["", data])
        digest = Crypto.Hash.SHA256.new()
        digest.update("\n".join(signeddata).encode("latin1"))
        return base64.b64encode(self.signer.sign(digest))
