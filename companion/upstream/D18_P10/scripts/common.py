from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def need(ok,message):
 if not ok:raise ValueError(message)
def load(path):return json.loads((ROOT/path).read_text(encoding='utf8'))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def emit(data):print(json.dumps(data,sort_keys=True,ensure_ascii=False),flush=True)
def rejected(action):
 try:action()
 except (ValueError,KeyError,TypeError,IndexError,EOFError):return True
 raise ValueError('Altered input was accepted')
