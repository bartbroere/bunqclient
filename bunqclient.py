import base64
import Crypto.PublicKey.RSA
import hashlib
import hmac
import json
import requests

class BunqClient(object):

    def __init__(base="https://api.bunq.com/v1",
                 secret=None,
                 **kwargs):
        self.base = base
        self.secret = secret
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
        self.headers = {}
        self.rsakey = Crypto.PublicKey.RSA.generate(2048)
        installation = self.request('installation',
                                    method="POST",
                                    data={"client_public_key":
                                          self.rsakey.publickey()})
        self.serverpublickey = installation["Response"][2]["ServerPublicKey"]
        self.token = installation["Response"][1]["Token"]["token"]
        self.deviceserver = self.request('device-server',
                                         method="POST",
                                         data={"description": "bunqclient",
                                               "secret": self.secret})
        self.deviceserver = self.deviceserver["Response"]["Id"]["id"]
        self.session = self.request('session-server',
                                    method="POST",
                                    data={"secret": self.secret})
        token = self.session["Response"]["Token"]["token"]
        self.headers["X-Bunq-Client-Authentication"] = token
        self.headers["Cache-Control"] = "no-cache"
        self.headers["User-Agent"] = "bunqclient 2017.7.4"
        self.headers["X-Bunq-Geolocation"] = "0 0 0 0 000"
        self.headers["X-Bunq-Language"] = "en_US"
        self.headers["X-Bunq-Region"}] = "nl_NL"
        return self

    def request(request, method="GET", data={}, **k):
        order = {self.hierarchy.index(idtype), idtype for idtype in k.keys()}
        elements = ["/".join([i, j]) for i, j in sorted(order.items())]
        url = "/".join([self.base].extend(elements))
        if request != "installation":
            self.headers["X-Bunq-Client-Request-Id"] = ""
            self.headers["X-Bunq-Client-Signature"] = sign(data)
        try: method = getattr(requests, method.lower)
        except AttributeError: method = requests.get


    def sign():
        return hmac.new(data,
                        key=self.privkey,
                        digestmod=hashlib.sha256).digest()
