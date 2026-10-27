"""Read-only collection of explicitly public, pinned portfolio sources."""
import hashlib, json, urllib.request, concurrent.futures
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / '.review' / 'sources'
CACHE.mkdir(parents=True, exist_ok=True)
SPECS = json.loads((ROOT / 'tools/sources.json').read_text())

def collect(spec):
    repo, path, name = spec['repo'], spec['path'], spec['cache']
    url = spec['source']
    req = urllib.request.Request(url, headers={'User-Agent': 'EngineeringArchive-review'})
    data = urllib.request.urlopen(req, timeout=40).read()
    blob = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
    assert blob == spec['blob_sha'], (name, 'public blob mismatch')
    (CACHE / name).write_bytes(data)
    return dict(repo=repo, path=path, source=url, blob_sha=blob, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), cache=name)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        result = list(pool.map(collect, SPECS))
    (ROOT / '.review/source-assets.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
