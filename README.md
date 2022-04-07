# FoxBit Client for Python

This is the README file for the Python client of the FoxBit exchange websocket API.

## Licensing
The software artifacts of this repository are licensed under [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0.html). A copy of the terms and conditions can be found in the [LICENSE](LICENSE) file.

## Requirements
	- Python >= 3.7
	- Websocket-client
	- Colorama

## Installation
Install dependencies and clone this repository:
```
python3 -m pip install --user websocket-client colorama && \
git clone https://github.com/femelo/foxbit-client-python.git
```

## Public endpoints
Inside the repository folder, instantiate client, connect, call endpoint. Example:
```
from foxbit_client import FoxBitClient
# Instantiate client
client = FoxBitClient()
# Connect
client.connect()
# Call endpoint
data = client.getInstruments(omsId=1)
print(data)
```

## Private endpoints
Instantiate client, authenticate user, call endpoint and log out. Example:
```
from foxbit_client import FoxBitClient
# Get environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
USERID = os.getenv("FOXBIT_USERID")
# Instantiate client
client = FoxBitClient()
# Connect
client.connect()
# Authenticate
client.authenticateUser(apiKey=API_KEY, apiSecret=API_SECRET, userId=USERID)
# Call endpoint
data = client.getUserPermissions(userId=client.userId)
print(data)
# Log out
client.logOut()
```
Note that in order to authenticate the user via API key and secret one must know the user ID. This can be done by authenticating via the methods webAuthenticateUser() and authenticate2FA() called in sequence. An example is provided in the script [foxbit_client_private_test.py](foxbit_client_private_test.py).
For complete reference, check https://foxbit.com.br/foxbit-api/.

## Test scripts
Two test scripts are provided to verify functionality of almost all public and private endpoints. These scripts can be run by
```
python3 foxbit_client_public_test.py
```
and, assuming the proper environment variables are set,
```
python3 foxbit_client_private_test.py
```