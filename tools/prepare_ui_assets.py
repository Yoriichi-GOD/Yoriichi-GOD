"""Optimize explicitly approved screenshots without cropping their viewports.

Original user PNGs remain untouched and ignored. Tracked WebP copies are both
the editable image inputs for the plate builder and the full-size click targets.
"""
import hashlib, json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'tools/ui_sources.json'
records=json.loads(manifest.read_text(encoding='utf-8'))
for record in records:
    source=ROOT/record['original']
    target=ROOT/record['output']
    if not source.is_file():
        if not target.is_file():raise FileNotFoundError(source)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==record['output_sha256']
        continue
    assert hashlib.sha256(source.read_bytes()).hexdigest()==record['original_sha256'], f'Changed source: {source.name}'
    im=Image.open(source).convert('RGB')
    im.thumbnail((1920,1920),Image.Resampling.LANCZOS)
    target.parent.mkdir(parents=True,exist_ok=True)
    im.save(target,format='WEBP',quality=90,method=6)
    record.update(output_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),output_dimensions=list(im.size),output_bytes=target.stat().st_size)
manifest.write_text(json.dumps(records,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{k:r[k] for k in ['slug','original_dimensions','output_dimensions','output_bytes']} for r in records],indent=2))
