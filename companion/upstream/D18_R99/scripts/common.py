from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def need(ok,message):
 if not ok:raise ValueError(message)
def load(name):return json.loads((ROOT/name).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rejected(call):
 try:call()
 except (ValueError,TypeError,KeyError,IndexError):return True
 raise ValueError('corrupted object was accepted')
def emit(obj):print(json.dumps(obj,sort_keys=True,ensure_ascii=False),flush=True)
