"""Shared I/O only; mathematical constructors remain separate."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,message):
    if not ok:raise ValueError(message)
def load(path):return json.loads((ROOT/path).read_text(encoding="utf8"))
def emit(obj):print(json.dumps(obj,sort_keys=True))
def rejected(fn):
    try:fn()
    except (ValueError,KeyError,IndexError,TypeError):return
    raise ValueError("deliberately invalid object was accepted")
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
