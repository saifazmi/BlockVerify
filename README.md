# BlockVerify

## About
This project uses Blockchain and OpenPGP to create a decentralised registry of file verification data. The registry contains the hash of the file, a signature confirming the ownership and the public key of the owner or author of the file. The signature is generated using OpenPGP, and the network is assumed to be a decentralised blockchain, making the data on the network immutable.

## Run the application
There are two separate applications that need to be started for the whole system to work:
- **API (Blockchain):** `src/api`
- **Client:** `src/client`

### Setup venv with python3
Navigate to the folders above in separate terminal windows. It is required to create a _virtual environment_ for _python_ before running the applications (for both directories):

```
$ python3 -m venv .venv
```

Activate the _virtual environment_:

```
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
```
(.venv) $ ./run.sh
 * Serving Flask app "blockAPI"
 * Running on http://127.0.0.1:6000/ (Press CTRL+C to quit)
```

#### Client

```
(.venv) $ ./run.sh
 * Serving Flask app "blockclient"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Clean up
Once you are done close the application with `Ctrl + C` and run the `./clean.sh` script and finally, to exit the virtual environment:

```
(.venv) $ deactivate
```
