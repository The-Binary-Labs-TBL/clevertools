# Installation

`clevertools` requires Python `>=3.11`.

## Fastest local install

If you are already inside a suitable virtual environment, this is enough:

```bash
pip install -e .
```

## Full development setup

### Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

### macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install -e .
```

### Windows Command Prompt

```bat
py -m venv .venv
.venv\Scripts\activate.bat
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install -e .
```

## What gets installed

- the `clevertools` package from `src/`
- the dependencies listed in `requirements.txt`
- an editable install so local source changes are available immediately

## Verify the installation

```bash
python -c "import clevertools; print(clevertools.__all__[:5])"
```

## Next steps

After installation, continue with:

1. [Getting Started](./getting-started.md)
2. [Quickstart](./quickstart.md)
3. [Tools](./tools/README.md)