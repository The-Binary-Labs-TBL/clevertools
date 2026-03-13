# clevertools

`clevertools` is a Python utility library for everyday filesystem and runtime tasks.

It provides:
- file and directory creation
- IO helpers
- cleanup helpers
- structured logging with console and file handlers
- runtime helpers and file bootstrapping
- a typed exception/validation model

## Start Working with it

1. Clone the repository (ssh recommended):
```bash
git clone git@github.com:The-Binary-Labs-TBL/clevertools.git
cd clevertools
```

2. Install all dependecies:

Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Project metadata is defined in `pyproject.toml`.

## Python version

- Required: `>=3.10`