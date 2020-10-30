import base64
from .bunqdefault import headers, hierarchy
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import json
import pickle
import requests
import uuid

class BunqClient:

    def __init__(self, base="https://api.bunq.com/v1", secret=""):
        self.base, self.secret = base, secret.encode("latin1")
        self.headers = headers()
        self.hierarchy = hierarchy()
        if secret != "": self.create_session()
        return

    def request(self, method="GET", data="", **k):
        url = self.prepare(**k)
        if type(data) == type(dict()): data = json.dumps(data)
        self.headers["X-Bunq-Client-Request-Id"] = str(uuid.uuid4())
        if "installation" not in k:
            self.headers["X-Bunq-Client-Signature"] = self.sign(
                url[len(self.base) - 3:], data=data, method=method).decode(
                'utf-8')
        try:
            method = getattr(requests, method.lower())
        except AttributeError:
            method = requests.get
        return json.loads(method(url, data=data, headers=self.headers).text)

    def sign(self, url, **k):
        signeddata = [" ".join([k.get("method", "GET"), url])]
        for header, value in sorted(self.headers.items()):
            if (header in ['Cache-Control', 'User-Agent']) or (
                    header[0:6] == "X-Bunq"):
                if header != "X-Bunq-Client-Signature":
                    signeddata.append(": ".join([header, value]))
        signeddata.extend(["", k.get("data", "")])
        sha256er = SHA256.new()
        sha256er.update("\n".join(signeddata).encode("latin1"))
        return base64.b64encode(self.signer.sign(sha256er))


    def prepare(self, **k):
        e = [self.base]
        o = {self.hierarchy.index(idtype): idtype for idtype in k.keys()}
        for _, i in sorted(o.items()): e.append("/".join([i, str(k[i])]))
        url = "/".join(e).replace("_", "-")
        return url[:-1] if url[-1] == "/" else url

    def create_rsasigner(self):
        self.rsakey = RSA.generate(2048)
        self.signer = PKCS1_v1_5.new(self.rsakey)

    def create_session(self, secret=None):
        if secret is not None: self.secret = secret
        self.create_rsasigner()
        self.installation = self.request(installation="", method="POST",
                                         data={"client_public_key": self.rsakey.publickey().exportKey(
                                         ).decode('utf-8').replace("RSA P", "P") + "\n"})
        self.headers["X-Bunq-Client-Authentication"] = self.installation[ \
            "Response"][1]["Token"]["token"]
        self.deviceserver = self.request(device_server="", method="POST",
                                         data={"description": "bunqclient",
                                               "secret": self.secret.decode('utf-8')})
        self.deviceserver = self.deviceserver["Response"][0]["Id"]["id"]
        self.session = self.request(session_server="", method="POST",
                                    data={"secret": self.secret.decode('utf-8')})
        self.headers["X-Bunq-Client-Authentication"] = self.session[ \
            "Response"][1]["Token"].get("token")

    def load_session(self, location):
        session = pickle.load(location)
        self.rsakey, self.signer = session[0], PKCS1_v1_5.new(session[0])
        self.headers["X-Bunq-Client-Authentication"] = session[1]

    def save_session(self, location):
        data = (self.rsakey, self.headers["X-Bunq-Client-Authentication"])
        pickle.dump(data, location)
