# HomeStake
HomeStake allows owners of a shared property to track loan progress, equity and any expenditures required for maintenance or rennovations.

The app consists of a REST API served via a FastAPI ASGI server, and a Postgres database, with models defined using SQLAlchemy.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation
This project requires `Python >= 3.12.2`, and it is recommended to use [pyenv](https://github.com/pyenv/pyenv) for Python version management.
```
homebrew install pyenv

# Can also run these steps for ~/.profile and ~/.bash_profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/$bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

pyenv install 3.12.2
pyenv local 3.12.2
```

### Other Prerequisites
To run the app server in a containerized environment the following are required to leverage the existing project deploy patterns:
* [Docker](https://docs.docker.com/engine/install/) (>= 20.10.21 recommended)
* [Docker Compose](https://docs.docker.com/compose/install/) (>= v2.13.0 recommended)

### Run Tests
```
make test # for direct local testing

make test-ci # for containerized testing
```

### Run Server
```
make deploy-local # for deploying server on host machine

make deploy-ci # for containerized deployment
```

## Usage
Invoking web endpopints with cURL:
```
$ curl localhost:8000/
Welcome to the HomeStake Equity and Contribution Tracker%
```

The entire API spec can be found at:
```
localhost:8000/docs
```

## License
[Apache-2.0 license](https://github.com/sprsld/homestake/blob/main/LICENSE)
