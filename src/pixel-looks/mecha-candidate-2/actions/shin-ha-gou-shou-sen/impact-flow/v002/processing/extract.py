from pathlib import Path
import subprocess,json,sys
r=Path('/workspace/work/mecha-impact-v002');id=sys.argv[1];source=sys.argv[2]
args=['python',str(r/'read.py'),'view','--image',source,'--request',str(r/f'ask-{id}'),'--name','pose-'+id,'--output-dir',str(r/f'extracted-{id}')];subprocess.run(args,check=True)
