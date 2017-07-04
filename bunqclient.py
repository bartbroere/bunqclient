import requests
import hashlib
import base64
import hmac
import json

class BunqSession(object):

    def __init__(base="https://api.bunq.com/v1/",
                 privkey=None,
                 **kwargs):
        self.base = base
        self.privkey = privkey
        self.apimethods = {"installation", "device", "device_server",
        "server-public-key", "ip", "credential-password-ip", "session",
        "session-server", "payment", "payment-batch", "request-inquiry", 
        "request-inquiry-batch", "request-response", "draft-payment",
        "schedule-payment", "schedule-payment-batch", "schedule-instance",
        "schedule", "tab-usage-single", "tab-usage-multiple", "tab-item",
        "tab-item-batch", "tab", "qr-code-content", "tab-result-inquiry",
        "tab-result-response", "mastercard-action", "TODO"}
        #TODO: generate public key
        #TODO: call installation
        #TODO: save returned session
        #TODO: register ip with device-server post
        #TODO: get a session token with POST /session-server
        return

    def request(method, request="GET", data={}):
        return

    def _sign():
        "Cache-Control"
        "User-Agent"
        "X-Bunq-Client-Authentication"
        "X-Bunq-Client-Request-Id"
        "X-Bunq-Geolocation"
        "X-Bunq-Language"
        "X-Bunq-Region"
        return hmac.new(data,
                        key=self.privkey,
                        digestmod=hashlib.sha256).digest()
