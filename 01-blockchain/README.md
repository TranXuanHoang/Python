# Blockchain app

[![Written In](https://img.shields.io/badge/Written%20in-Python-blue?style=flat-square)](https://python.org/)
[![Web Framework](https://img.shields.io/badge/Web%20Framework-Flask-orange?style=flat-square)](https://palletsprojects.com/p/flask/)
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
| [pycryptodome](https://pypi.org/project/pycryptodome/) | Utilize `encryption` and/or `decryption` algorithms on Windows |
| [Flask](https://pypi.org/project/Flask/) | Serve and handle HTTP requests |
| [Flask-Cors](https://pypi.org/project/Flask-Cors/) | Handle `Cross Origin Resource Sharing` (CORS) and make cross-origin AJAX possible |

## APIs List

The app provides the following APIs:

| API Endpoint | Description |
|--------------|-------------|
| ```GET: /chain``` | **Fetch blockchain:** Fetch the whole blockchain. <pre lang="shell">curl --location --request GET 'http://localhost:5000/chain'</pre> |
| ```POST: /mine``` | **Mine a new block:** Mine a new block by adding all open transactions into a new block, then add that block into the blockchain. <pre lang="shell">curl --location --request POST 'http://localhost:5000/mine' </pre> |
| ```POST /wallet``` | **Create wallet keys:** Create a pair of public and private keys, then save them in a file. <pre lang="shell">curl --location --request POST 'http://localhost:5000/wallet'</pre> |
| ```GET /wallet``` | **Load wallet keys:** Load the public and private keys of the wallet. <pre lang="shell">curl --location --request GET 'http://localhost:5000/wallet'</pre> |
| ```GET /balance``` | **Load the current balance:** Load the current balance of remaining coins in the wallet. <pre lang="shell">curl --location --request GET 'http://localhost:5000/balance'</pre> |
| ```POST /transaction``` | **Make a new transaction:** Add a new transaction sending an `amount` of coins to a `recipient`. </br> **Request Header:** `Content-Type: application/json` </br>**Body:** `{ "recipient": "Bob", "amount": 7.5 }` <pre lang="shell">curl --location --request POST 'http://localhost:5000/transaction' --header 'Content-Type: application/json' --data-raw '{"recipient": "Bob", "amount": 7.5}'</pre> |
| ```GET /transactions``` | **Fetch transactions:** Fetch all open transactions available for mining. <pre lang="shell">curl --location --request GET 'http://localhost:5000/transactions'</pre> |
| ```POST /node``` | **Add a new node:** Add a new node to the set of connected nodes. </br> **Request Header:** `Content-Type: application/json` </br>**Body:** `{"node": "node_url"}` <pre lang="shell">curl -X POST http://localhost:5000/node -H 'content-type: application/json' -d '{"node": "localhost:5001"}'</pre> |
| ```DELETE /node/<node_url>``` | **Delete a node:** Delete a node from the set of connected nodes. <pre lang="shell">curl -X DELETE http://localhost:5000/node/localhost:5001</pre> |
| ```GET /nodes``` | **Get all connected nodes:** Fetch a list of all connected nodes. <pre lang="shell">curl -X GET http://localhost:5000/nodes</pre> |

## App Snapshot

<p align="center">
    <img src="./docs/AppSnapshot.gif" width="65%"/>
</p>
