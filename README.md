# BlockVerify

## About

This project uses Blockchain and OpenPGP to create a decentralised registry of file verification data. The registry contains the hash of the file, a signature confirming the ownership and the public key of the owner or author of the file. The signature is generated using OpenPGP, and the network is assumed to be a decentralised blockchain, making the data on the network immutable.

## Pre-requisites

### Required

[Gnupg](https://gnupg.org/) binary for your operating system.

I tested the python library [gnupg](https://pypi.python.org/pypi/gnupg) in this simple script: [/prototypes/gpg.py](https://github.com/saifazmi/BlockVerify/blob/master/prototypes/gpg.py) and from what I can tell it only seems to work with `gpg1` or gnupg1 package. For reference this is the package that I used https://aur.archlinux.org/packages/gnupg1/ download a similar one for your OS.

You can also configure the path to the `gpg` binary via the environment variable [GPG_BINARY](#GPG_BINARY)

### Optional

[sqlite3](https://www.sqlite.org/index.html) database for a quick start.

I use SQLite for testing the application but you can plugin any DB that you want using the environment variable [SQLALCHEMY_DATABASE_URI](#SQLALCHEMY_DATABASE_URI) on both the client and the API.

## Environment variables

All of these variables have defaults, but if you want to use something else, please feel free to define the values for these environment variables and the code will pick them up.

If you don't know what enironement variables are or how to define them, then refer to this: [Environment_variable#Assignment](https://en.wikipedia.org/wiki/Environment_variable#Assignment)

### API

**Config file:** `src/api/config.py`

#### SQLALCHEMY_DATABASE_URI

This allows you to define which database program to use for the API and the path to the DB.
**Default:** sqlite:///src/api/app.db

### Client

**Config file:** `src/client/config.py`

#### SQLALCHEMY_DATABASE_URI

This allows you to define which database program to use for the Client and the path to the DB.
**Default:** sqlite:///src/client/app.db

#### GPG_BINARY

Using this you can define the path to the desired `gpg` binary to be used by the `gnupg` python library.
**Default:** /usr/bin/gpg1

#### GPG_KEY_STORE

Used for defining where the GPG key store (key database) is stored. This can be stored on another secure node rather than the client for more security, hence this option.
**Default:** src/client/keys

#### SECRET_KEY

This is the secret key used for generating [CSRF](https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)) tokens for forms. This is a security feature and I suggest that you use your own key.
**Default:** "your-secret-key"

#### UPLOAD_FOLDER

This defines the path to the folder where files are stored temporarily for processing (generating file hash) and then deleted right after that. This is for both adding and verifying a file.
**Default:** src/client/uploads

## Run the application

There are two separate applications that need to be started for the whole system to work:

- **API (Blockchain):** `src/api`
- **Client:** `src/client`

### Setup venv with python3

Navigate to the folders above in separate terminal windows. It is required to create a _virtual environment_ for _python_ before running the applications (for both directories):

```bash
$ python3 -m venv .venv
```

Activate the _virtual environment_:

```bash
$ source .venv/bin/activate
```

> **NOTE:** Before processding make sure that the terminal prompt looks like this: `(.venv) $`

Both the API and the Client come with three bash scripts:

- `setup.sh`: installs the required python dependencies, configures flask and create database.
- `run.sh`: starts the application.
- `clean.sh`: deletes the database.

> **NOTE:** the API application needs to be running for the Client to work as expected.

### Start the applications

For a fresh setup run the `./setup.sh` script followed by `./run.sh` and the terminal output should look like this:

#### API

```bash
(.venv) $ ./run.sh
 * Serving Flask app "blockAPI"
 * Running on http://127.0.0.1:6000/ (Press CTRL+C to quit)
```

#### Client

```bash
(.venv) $ ./run.sh
 * Serving Flask app "blockclient"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Important note:

Once you have added a file, it is not automatically added to the blockchain. The chain needs to be **mined**, if you search for the file before mining it will not be found (404). For the purposes of this demo program the mining process has to be triggered manually. You can automate this later when you are running nodes to form consensus.

Generally you will have multiple files in the transaction pool ready to be mined and added to a block in the blockchain. But when you are testing you can call the following endpoint after adding the first file to test the verification mechanism after that.

For now you need to call the API endpoint: `/api/mine`

**CURL**
```bash
$ curl --location --request GET "http://localhost:6000/api/mine"
```

### Clean up

Once you are done close the application with `Ctrl + C` and run the `./clean.sh` script and finally, to exit the virtual environment:

```bash
(.venv) $ deactivate
```

## API Reference

https://documenter.getpostman.com/view/3186515/RW1aJfNe
