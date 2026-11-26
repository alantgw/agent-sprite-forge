from pathlib import Path
import json,subprocess,concurrent.futures
r=Path('/workspace/work/mecha-impact-v003');rows=json.loads((r/'generation-records.json').read_text())
def one(row):
 id=row['id'];out=r/f'extracted-{id}'
 if (out/f'pose-{id}.json').exists():return id,'already extracted'
 p=subprocess.run(['python',str(r/'extract.py'),id,row['source']],text=True,capture_output=True);return id,p.stdout.strip() or p.stderr[-800:]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for id,result in pool.map(one,rows):print(id,result)
