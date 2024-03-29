Now archived and not maintained.
Check out [the official Python SDK for the Bunq API](https://github.com/bunq/sdk_python) instead:
https://github.com/bunq/sdk_python

<hr></hr>


# bunqclient
Python client for the bunq public API.

![Build status](https://img.shields.io/travis/bartbroere/bunqclient.svg)
![Code Climate](https://codeclimate.com/github/bartbroere/bunqclient.svg)
![Release](https://img.shields.io/pypi/v/bunqclient.svg)
![Pre-release](https://img.shields.io/github/release/bartbroere/bunqclient/all.svg)
![Licence](https://img.shields.io/pypi/l/bunqclient.svg)
![Versions](https://img.shields.io/pypi/pyversions/bunqclient.svg)

## Installation
Installing the latest release can be done from PyPi:
```
pip install bunqclient
```

The latest unreleased version can be installed from GitHub:
```
git clone https://github.com/bartbroere/bunqclient/
cd ./bunqclient
python setup.py install
```

## Usage
Before using it, make sure that you understand the cost scheme of this API. 
Replace the value of the parameter ``secret`` with the API key generated in
the bunq app.

```python
from bunqclient import BunqClient
bunq = BunqClient(secret="")
```

To use the sandbox version change the ``base`` parameter. Note that you should
use a separate API key for this. A sandbox key can be acquired by asking bunq
support.

```python
from bunqclient import BunqClient
bunq_sandbox = BunqClient(base="https://sandbox.public.api.bunq.com/v1", 
                          secret="")
```

``LIST`` requests are basically ``GET`` requests without a specified key. The 
first two API calls have the same effect. The third requests a specific 
``monetary-account``. Due to the way Python interprets variable names, dashes
(``-``) in API methods and keys should be replaced with underscores (``_``).

```python
bunq.request(method="LIST", monetary_account="", user=1)
bunq.request(method="GET", monetary_account="", user=1)
bunq.request(method="GET", monetary_account=11, user=1)
```

These API calls return a python dictionary with the query's result.

## Contributing
To report bugs and submit feature requests, please open an issue on GitHub.
Pull requests that resolve issues or TODO's are also greatly appreciated.
