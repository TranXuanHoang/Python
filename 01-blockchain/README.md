# Blockchain app

[![Written In](https://img.shields.io/badge/Written%20in-Python-blue?style=flat-square)](https://python.org/)
[![Web Framework](https://img.shields.io/badge/Web%20Framework-Flask-orange?style=flat-square)](https://palletsprojects.com/p/flask/)
[![Make HTTP Requests](https://img.shields.io/badge/Make%20HTTP%20Requests%20with-Requests-9B59B6?style=flat-square)](https://requests.readthedocs.io/)
[![Blockchain](https://img.shields.io/badge/Blockchain-16A085?style=flat-square)](https://en.wikipedia.org/wiki/Blockchain)
[![Cryptocurrency](https://img.shields.io/badge/Cryptocurrency-16A085?style=flat-square&logo=bitcoin)](https://en.wikipedia.org/wiki/Cryptocurrency)

Construct a blockchain app which can safely manage cryptocurrency coins and transactions. The app implements a blockchain to save all mined blocks of coins transfering transactions and uses some encryption/decryption algorithms to validate and maintain its data integrity.

## Required Third-Party Packages

Beside the [Python](https://www.python.org/) standard libraries, this app also needs the following packages installed globally in your machine (or locally in a virtual Python environment) in order to function correctly.

> **_Note 1:_** Ensuring pip, setuptools, and wheel are up to date before installing packages is recommended. For more information, head over to [this page](https://packaging.python.org/tutorials/installing-packages/#ensure-pip-setuptools-and-wheel-are-up-to-date).
>
> `python -m pip install --upgrade pip setuptools wheel`
>
> If your OS is Windows, you may need to install Windows C++ compilers in some cases. See [this wiki page](https://wiki.python.org/moin/WindowsCompilers) for the instructions.
>
> **_Note 2:_** Another solution for managing Python packages is [Anaconda](https://www.anaconda.com/). [Anaconda Individual Edition](https://www.anaconda.com/products/individual) provides a simple way of installing and managing Python packages as well as launching apps in different virtual environments and _it is free (at the time of writing this readme file)_.

| Package | Purpose |
| --------| --------|
| [pycrypto](https://pypi.org/project/pycrypto/) | Utilize `encryption` and/or `decryption` algorithms |
| [pycryptodome](https://pypi.org/project/pycryptodome/) | Utilize `encryption` and/or `decryption` algorithms (quite stable on Windows) |
| [Flask](https://pypi.org/project/Flask/) | Serve and handle HTTP requests |
| [Flask-Cors](https://pypi.org/project/Flask-Cors/) | Handle `Cross Origin Resource Sharing` (CORS) and make cross-origin AJAX possible |
| [requests](https://pypi.org/project/requests/) | Make HTTP requests inside Python code |

## APIs List

The app provides the following APIs:

| API Endpoint | Description |
|--------------|-------------|
| ```GET: /chain``` | **Fetch blockchain:** Fetch the whole blockchain. <pre lang="shell">curl -X GET 'http://localhost:5000/chain'</pre> |
| ```POST: /mine``` | **Mine a new block:** Mine a new block by adding all open transactions into a new block, then add that block into the blockchain. <pre lang="shell">curl -X POST 'http://localhost:5000/mine' </pre> |
| ```POST /wallet``` | **Create wallet keys:** Create a pair of public and private keys, then save them in a file. <pre lang="shell">curl -X POST 'http://localhost:5000/wallet'</pre> |
| ```GET /wallet``` | **Load wallet keys:** Load the public and private keys of the wallet. <pre lang="shell">curl -X GET 'http://localhost:5000/wallet'</pre> |
| ```GET /balance``` | **Load the current balance:** Load the current balance of remaining coins in the wallet. <pre lang="shell">curl -X GET 'http://localhost:5000/balance'</pre> |
| ```POST /transaction``` | **Make a new transaction:** Add a new transaction sending an `amount` of coins to a `recipient`. </br> **Request Header:** `Content-Type: application/json` </br>**Body:** `{ "recipient": "Bob", "amount": 7.5 }` </br></br> <code lang="shell"> curl -X POST 'http://localhost:5000/transaction' </br> -H 'Content-Type: application/json' </br> -d '{"recipient": "Bob", "amount": 7.5}'</code> |
| ```GET /transactions``` | **Fetch transactions:** Fetch all open transactions available for mining. <pre lang="shell">curl -X GET 'http://localhost:5000/transactions'</pre> |
| ```POST /node``` | **Add a new node:** Add a new node to the set of connected nodes. </br> **Request Header:** `Content-Type: application/json` </br>**Body:** `{"node": "node_url"}` </br></br> <code lang="shell"> curl -X POST 'http://localhost:5000/node' </br> -H 'content-type: application/json' </br> -d '{"node": "localhost:5001"}'</code> |
| ```DELETE /node/<node_url>``` | **Delete a node:** Delete a node from the set of connected nodes. <pre lang="shell">curl -X DELETE 'http://localhost:5000/node/localhost:5001'</pre> |
| ```GET /nodes``` | **Get all connected nodes:** Fetch a list of all connected nodes. <pre lang="shell">curl -X GET 'http://localhost:5000/nodes'</pre> |
| ```POST /broadcast-transaction``` | **Broadcast a transaction:** Broadcast a new transaction to other nodes. </br> **Request Header:** `Content-Type: application/json` </br>**Body:** `{"sender": "...", "recipient": "...", "amount": ..., "signature": "..."}`</br></br> <code lang="shell"> curl -X POST 'http://localhost:5001/broadcast-transaction' </br> -H 'content-type: application/json' </br> -d '{</br> "sender": "sender's public key",</br> "recipient": "recipient's public key",</br> "amount": ...,</br> "signature": "signature of transaction"</br> }'</code> |
| ```POST /broadcast-block``` | **Broadcast a block:** Broadcast a new block to other nodes. </br> **Request Header:** `Content-Type: application/json` </br>**Body:** <code lang="shell">{"block": {"index": ..., "previous_hash": "...", "timestamp": ..., "transactions": [...], "proof": ...}}</code></br></br> <code lang="shell"> curl -X POST 'http://localhost:5001/broadcast-block' -H 'content-type: application/json' -d '{"block": ...}' </code> |
| ```POST /resolve-conflicts``` | **Resolve blockchain conflicts:** Resolve blockchain conflicts among peer nodes in the nodes network. </br></br> <pre lang="shell"> curl -X POST 'http://localhost:5001/resolve-conflicts' </pre> |

## Run App

This documentation decribes steps to use [Anaconda Individual Edition](https://www.anaconda.com/products/individual) to install packages and run the app on a virtual Python environment.

* Download and [install Anaconda](https://docs.anaconda.com/anaconda/install/), then create a new environemt named like `pycoin` with Anaconda. See [this page](https://docs.anaconda.com/anaconda/navigator/tutorials/manage-environments/) for instructions. Install all required packages described in the [Required Third-Party Packages](#required-third-party-packages) section in the newly created environment using the [Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/) which is automatically installed when you install Anaconda.

* Activate the virtual environment (_MacOS_ or _Linux_): Runinng `source activate NAME_OF_ENVIRONMENT` (e.g. `source activate pycoin`) to activate the environment.

* Activate the virtual environment (_Windows_): You can use activate the virtual environment using the Anaconda Navigator GUI. If you, however, want to activate the environment and run the app with Windows's PowerShell, the following commands are your start-to-go (remember to change the values of `USER_NAME` and `NAME_OF_ENVIRONMENT` to yours, and change the `path`s of other environment variables if they differ on your machine. The commands here were tested on a real Windows PC):<pre lang="shell">
$Env:USER_NAME = "hoang.tran"
$Env:NAME_OF_ENVIRONMENT = "pycoin"
$Env:_CONDA_ROOT = "C:/Users/$Env:USER_NAME/Anaconda3"
$Env:CONDA_EXE = "$Env:_CONDA_ROOT/Scripts/conda.exe"
$Env:_CONDA_EXE = "$Env:_CONDA_ROOT/Scripts/conda.exe"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
Import-Module "$Env:_CONDA_ROOT/shell/condabin/Conda.psm1"
Add-CondaEnvironmentToPrompt
conda activate "$Env:_CONDA_ROOT" ; conda activate $Env:NAME_OF_ENVIRONMENT
</pre>

* Start the app: `cd` into the dicretory of the `node.py` file, then run one of the following commands (e.g. `python node.py -p 5001`):<pre>`python node.py`<br>`python node.py -p port_num`<br>`python node.py --port port_num`</pre>
Then open browser and load `localhost:5000` for the app started with `python node.py` or load `localhost:port_num` for the app started with `python node.py [-p|--port] port_num`

## App Snapshot

<p align="center">
    <img src="./docs/AppSnapshot.gif" width="65%"/>
</p>
