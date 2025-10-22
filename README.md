# Flight Price Tracker

This project uses Python 3.12 and can be installed using **uv** or traditional **pip**.

## Using uv (recommended)

```bash
# Clone the project
git clone https://github.com/khaibom/Flight-Price-Tracker.git
cd flight-price-tracker
```
```bash
# Create virtual environment using uv
uv venv .venv
```
```bash
.venv\Scripts\activate  # Windows
```
```bash
source .venv/bin/activate  # macOS/Linux
```
```bash 
# Install dependencies exactly as in uv.lock
uv sync
```

## Using pip (alternative)

```bash
# Clone the project
git clone https://github.com/khaibom/Flight-Price-Tracker.git
cd flight-price-tracker
```
```bash
# Create a standard virtual environment
python -m venv .venv
```
```bash
.venv\Scripts\activate  # Windows
```
```bash
source .venv/bin/activate  # macOS/Linux
```
```bash
# Install dependencies via pip
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
