# BlockVerify

There are two separate applications that need to be started for the whole system to work:
- API (Blockchain): `src/api`
- Client: `src/client`

## Setup venv with python3
Navigate to the folders above in separate terminal windows. It is required to create a virtual environment for python before running the applications (for both directories):

```
$ python3 -m venv .venv
```

Activate the virtual environment:

```
$ source .venv/bin/activate
```

> **NOTE:** Make sure that the terminal prompt looks like the following before proceeding:
`(.venv) $`

Both the API and the Client come with three bash scripts:
- setup.sh: installs the required python dependencies, configures flask and create database.
- run.sh: starts the application.
- clean.sh: deletes the database

> **NOTE:** the API application needs to be running for the Client to work as expected.

## Start the applications

For a fresh setup run the `./setup.sh` script followed by `./run.sh` and the terminal output should look like this:

### API
```
(.venv) $ ./run.sh
 * Serving Flask app "blockAPI"
 * Running on http://127.0.0.1:6000/ (Press CTRL+C to quit)
```

### Client

```
(.venv) $ ./run.sh
 * Serving Flask app "blockclient"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Clean up
Once you are done close the application with Ctrl + C and run the ./clean.sh script and finally:

```
(.venv) $ deactivate
```

To exit the virtual environment.
