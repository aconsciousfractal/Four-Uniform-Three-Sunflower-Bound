"""Shared I/O only; mathematical generators remain separate."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def need(ok,message):
    if not ok:raise ValueError(message)
def load(name):return json.loads((ROOT/name).read_text(encoding='utf8'))
def emit(obj):print(json.dumps(obj,sort_keys=True))
def rejected(f):
    try:f()
    except (ValueError,KeyError,IndexError,TypeError) as e:return str(e)
    raise ValueError('deliberate corruption accepted')
