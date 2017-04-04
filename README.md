# Score Engine
Scoring Engine used for UBNETDEF's [Lockdown](https://lockdown.ubnetdef.org) Competition.

## Requirements
* python 2.7
* Every python module in "requirements.txt"

## Package Requirements
```python-dev libmysqlclient-dev libsasl2-dev python-dev libldap2-dev libssl-dev```

## Installation
* Clone this repository
* Copy `config.py-dist` to `config.py`
* Edit `config.py` to fit your deployment
* Run `pip install -r requirements.txt`
* Run `python ./setup.py`

## How to use
Simply run `python ./start.py`, and hope for the best

## Notes
If you wish to run an individual check, run "`python ./check.py`" with the TEAM ID and SERVICE ID as arguments.  This will not save to the database.
