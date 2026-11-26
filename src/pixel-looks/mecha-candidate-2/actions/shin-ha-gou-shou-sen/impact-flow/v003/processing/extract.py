from pathlib import Path
import subprocess,sys,json
r=Path('/workspace/work/mecha-impact-v003');id=sys.argv[1];source=sys.argv[2];row=next(q for q in json.loads((r/'plan.json').read_text()) if q['id']==id)
subprocess.run(['python',str(r/'read.py'),'view','--image',source,'--request',row['request'],'--name','pose-'+id,'--output-dir',str(r/f'extracted-{id}')],check=True)
